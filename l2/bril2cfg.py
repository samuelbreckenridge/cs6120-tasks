import json
import sys
from dataclasses import dataclass


@dataclass
class CFG:
    """Represents a control flow graph for a function"""

    blocks: list[list[dict]]
    successors: dict[int, list[int]] # maps a block index to a list of the indices of its successors

    @classmethod
    def from_blocks(cls, blocks: list[list[dict]]):
        """Parse a list of blocks to generate the CFG"""
        label_to_block_index = {}
        successors = {}
        for i, block in enumerate(blocks):
            if "label" in block[0]:
                label_to_block_index[block[0]["label"]] = i
        for i, block in enumerate(blocks):
            terminator = block[-1]
            if "op" not in terminator:
                # Handle block consisting of a single label
                successors[i] = [i+1]
            else:
                if terminator["op"] == "ret" or i == len(blocks) - 1:
                    # Returns and final block have a common successor
                    successors[i] = [len(blocks)]
                elif terminator["op"] in ["jmp", "br"]:
                    successors[i] = [label_to_block_index[l] for l in terminator["labels"]]
                else:
                    successors[i] = [i+1]
        return cls(blocks, successors)

    def __repr__(self) -> str:
        out = ""
        for i, block in enumerate(self.blocks):
            out += f"Block {i}:\n"
            out += f"\tinstrs: {block}\n"
            out += f"\tsuccessors: {self.successors[i]}\n"
        return out


def generate_basic_blocks(bril_func: dict) -> list[list[dict]]:
    blocks = []
    current_block = []
    for instr in bril_func["instrs"]:
        if "op" in instr:
            current_block.append(instr)
            if instr["op"] in ["jmp", "br", "ret"]:
                # Terminator
                blocks.append(current_block)
                current_block = []
        else:
            # Label
            if current_block:
                blocks.append(current_block)
            current_block = [instr]
    if current_block:
        blocks.append(current_block)
    return blocks


if __name__ == "__main__":
    bril_json = json.loads(sys.stdin.read())
    for func in bril_json["functions"]:
        basic_blocks = generate_basic_blocks(func)
        cfg = CFG.from_blocks(basic_blocks)
        print(func["name"])
        print(cfg)
