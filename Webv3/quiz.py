# Quiz Program - Computer Systems & Assembly
# Author: Roberto Guallichico

QUESTIONS = [
    {
        "question": "What is a byte?",
        "choices": [
            "4 bits",
            "8 bits grouped together",
            "16 bits",
            "1 kilobyte"
        ],
        "answer": "b",
        "explanation": "A byte is the standard unit of storage and represents 8 bits combined."
    },
    {
        "question": "What is a source program?",
        "choices": [
            "Machine code",
            "a program written in a high-level programming language",
            "Binary file",
            "Instruction set"
        ],
        "answer": "b",
        "explanation": "A source program is human-readable code written in languages like C, Java, or Python."
    },
    {
        "question": "What are the steps of the compilation system?",
        "choices": [
            "compiler, assembler, optimizer, loader",
            "preprocessor, compiler, assembler, and linker",
            "editor, compiler, debugger, linker",
            "tokenizer, interpreter, executor, linker"
        ],
        "answer": "b",
        "explanation": "The compilation process transforms high-level code into machine code through these four stages."
    },
    {
        "question": "In which step of the compilation system does the code go from a text file to binary?",
        "choices": [
            "preprocessing",
            "compilation",
            "assembly",
            "linking"
        ],
        "answer": "c",
        "explanation": "During assembly, assembly language is translated into binary machine code."
    },
    {
        "question": "T or F: Each statement of assembly language corresponds to a single machine code.",
        "choices": [
            "True",
            "False",
            "Sometimes",
            "Depends on the CPU"
        ],
        "answer": "a",
        "explanation": "Assembly has a one-to-one mapping with machine instructions."
    },
    {
        "question": "T or F: Code written in assembly language is very portable.",
        "choices": [
            "True",
            "False",
            "Only for RISC",
            "Only for CISC"
        ],
        "answer": "b",
        "explanation": "Assembly is tied to the instruction set of a specific machine, so it is not portable."
    },
    {
        "question": "What are the two parts of a computer system?",
        "choices": [
            "CPU and GPU",
            "hardware and software",
            "memory and storage",
            "input and output"
        ],
        "answer": "b",
        "explanation": "Hardware is the physical equipment, and software is the set of programs that run on it."
    },
    {
        "question": "What is the interface between the computer's hardware and software?",
        "choices": [
            "Operating system",
            "Application programming interface",
            "ISA (instruction set architecture)",
            "Device driver"
        ],
        "answer": "c",
        "explanation": "The ISA defines the commands that software can use to control hardware."
    },
    {
        "question": "What are the two subsets of computer software?",
        "choices": [
            "Firmware and middleware",
            "Operating system and application programs",
            "Productivity and entertainment",
            "System and utility"
        ],
        "answer": "b",
        "explanation": "The operating system manages resources, while applications perform user tasks."
    },
    {
        "question": "What is SSD short for?",
        "choices": [
            "Solid State Drive",
            "Sequential Storage Disk",
            "Static System Device",
            "Single Storage Drive"
        ],
        "answer": "a",
        "explanation": "SSD is a nonvolatile storage device that is faster than traditional hard drives."
    },
    {
        "question": "Describe memory hierarchy.",
        "choices": [
            "Cache, Register, Main Memory, Secondary Storage",
            "Register, Cache, Main Memory, Secondary Storage",
            "Register, Main Memory, Cache, Secondary Storage",
            "Secondary Storage, Main Memory, Cache, Register"
        ],
        "answer": "b",
        "explanation": "Registers and cache are on-chip (fastest), followed by main memory and then slower storage devices."
    },
    {
        "question": "T or F: Everything is represented as a sequence of binary numbers in digital systems.",
        "choices": [
            "True",
            "False",
            "Only for data, not instructions",
            "Only for numbers"
        ],
        "answer": "a",
        "explanation": "All data in digital systems is encoded in binary (0s and 1s)."
    },
    {
        "question": "Is one represented as high or low voltage?",
        "choices": [
            "High",
            "Low",
            "Either, depending on the system",
            "No voltage"
        ],
        "answer": "a",
        "explanation": "Digital logic usually uses high voltage to represent 1."
    },
    {
        "question": "Is 0 represented as high or low voltage?",
        "choices": [
            "High",
            "Low",
            "Either, depending on the system",
            "Negative voltage"
        ],
        "answer": "b",
        "explanation": "Digital logic usually uses low voltage to represent 0."
    },
    {
        "question": "What is a memory address?",
        "choices": [
            "A unique number identifying the location of the byte in memory",
            "The name of a variable",
            "A pointer to a function",
            "The size of memory"
        ],
        "answer": "a",
        "explanation": "Each byte in memory has a unique address for identification."
    },
    {
        "question": "How is word size determined?",
        "choices": [
            "By the compiler settings",
            "By the size of data the machine is designed for",
            "By the operating system",
            "By the hard drive capacity"
        ],
        "answer": "b",
        "explanation": "Word size depends on the CPU architecture, commonly 64 bits today."
    },
    {
        "question": "What size is a pointer?",
        "choices": [
            "Always 4 bytes",
            "Always 8 bytes",
            "The same size as the word",
            "Half the size of the word"
        ],
        "answer": "c",
        "explanation": "Pointers must be large enough to store any memory address, so they match the word size."
    },
    {
        "question": "How is Big Endian ordered?",
        "choices": [
            "Most significant byte has highest address",
            "Least significant byte has highest address",
            "Most significant byte has lowest address",
            "Least significant byte has lowest address"
        ],
        "answer": "b",
        "explanation": "Big Endian stores the most significant byte at the lowest address, and the least significant at the highest."
    },
    {
        "question": "How is Little Endian ordered?",
        "choices": [
            "Most significant byte has highest address",
            "Least significant byte has highest address",
            "Most significant byte has lowest address",
            "Least significant byte has lowest address"
        ],
        "answer": "d",
        "explanation": "Little Endian stores the least significant byte at the lowest address, and the most significant at the highest."
    },
    {
        "question": "What is the significance of a variable declared 'T *x;'?",
        "choices": [
            "It declares a structure",
            "It declares a pointer to type T",
            "It declares an array",
            "It declares a reference"
        ],
        "answer": "b",
        "explanation": "The asterisk * declares a pointer, which stores the address of a value rather than the value directly."
    },
    {
        "question": "What is Moore's Law?",
        "choices": [
            "Processor speed doubles every month",
            "The number of transistors doubles every 18-24 months",
            "Memory capacity triples every year",
            "Power consumption halves every decade"
        ],
        "answer": "b",
        "explanation": "Moore's Law observes the exponential growth of computing power over time."
    },
    {
        "question": "What is PC short for?",
        "choices": [
            "Program Code",
            "Processor Clock",
            "Program Counter",
            "Process Control"
        ],
        "answer": "c",
        "explanation": "The program counter stores the address of the next instruction to be executed."
    },
    {
        "question": "Registers store what?",
        "choices": [
            "Archived data",
            "User files",
            "Heavily used program data",
            "Machine code comments"
        ],
        "answer": "c",
        "explanation": "Registers are very fast memory used to store critical values during execution."
    },
    {
        "question": "What stores status information about the most recent arithmetic operation?",
        "choices": [
            "Instruction register",
            "Stack pointer",
            "Condition code",
            "Base pointer"
        ],
        "answer": "c",
        "explanation": "Condition codes indicate results such as zero, negative, overflow, etc."
    },
    {
        "question": "T or F: Condition code is not used for conditional branching.",
        "choices": [
            "True",
            "False",
            "Only on RISC processors",
            "Only on CISC processors"
        ],
        "answer": "b",
        "explanation": "Condition codes are used directly in conditional jumps and branches."
    },
    {
        "question": "What are the three basic operations of machine code?",
        "choices": [
            "Input, processing, output",
            "Arithmetic and logic, memory/data movement, control flow",
            "Fetch, decode, execute",
            "Compile, assemble, link"
        ],
        "answer": "b",
        "explanation": "Machine code supports calculations, memory access, and program control."
    },
    {
        "question": "CISC or RISC? Large number of instructions.",
        "choices": [
            "CISC",
            "RISC",
            "Both",
            "Neither"
        ],
        "answer": "a",
        "explanation": "CISC processors implement many specialized instructions."
    },
    {
        "question": "CISC or RISC? Small number of instructions.",
        "choices": [
            "CISC",
            "RISC",
            "Both",
            "Neither"
        ],
        "answer": "b",
        "explanation": "RISC processors use a simplified instruction set for efficiency."
    },
    {
        "question": "CISC or RISC? Varying instruction length.",
        "choices": [
            "CISC",
            "RISC",
            "Both",
            "Neither"
        ],
        "answer": "a",
        "explanation": "CISC instructions vary in length, while RISC has fixed-length instructions."
    },
    {
        "question": "CISC or RISC? Compact code size.",
        "choices": [
            "CISC",
            "RISC",
            "Both",
            "Neither"
        ],
        "answer": "a",
        "explanation": "CISC's many instructions often result in smaller program sizes."
    },
    {
        "question": "CISC or RISC? Large code size.",
        "choices": [
            "CISC",
            "RISC",
            "Both",
            "Neither"
        ],
        "answer": "b",
        "explanation": "RISC code is more verbose because complex operations require multiple simple instructions."
    },
    {
        "question": "What type of operand deals with constant data?",
        "choices": [
            "Immediate operand",
            "Register operand",
            "Memory operand",
            "Pointer operand"
        ],
        "answer": "a",
        "explanation": "Immediate operands are fixed values embedded directly in instructions."
    },
    {
        "question": "What type of operand deals with an integer register?",
        "choices": [
            "Immediate operand",
            "Register operand",
            "Memory operand",
            "Flag operand"
        ],
        "answer": "b",
        "explanation": "Register operands directly reference CPU registers for fast access."
    },
    {
        "question": "What type of operand deals with 8 consecutive bytes?",
        "choices": [
            "Immediate operand",
            "Register operand",
            "Memory operand",
            "Vector operand"
        ],
        "answer": "c",
        "explanation": "Memory operands reference data stored in memory rather than registers or constants."
    }
]

CHOICE_LABELS = ["a", "b", "c", "d"]


def run_quiz() -> None:
    """Run the quiz game in the terminal."""

    print("\n=== Computer Systems & Assembly Quiz ===\n")

    for index, item in enumerate(QUESTIONS, start=1):
        print(f"Question {index}: {item['question']}")
        for label, choice in zip(CHOICE_LABELS, item["choices"]):
            print(f"  {label}) {choice}")

        while True:
            user_answer = input("Your answer (a/b/c/d): ").strip().lower()
            if user_answer not in CHOICE_LABELS:
                print("❌ Error, try again.")
                continue

            if user_answer == item["answer"]:
                print("✅ Correct!")
                print(f"Explanation: {item['explanation']}\n")
                break

            print("❌ Error, try again.")

    print("🎉 Quiz complete!\n")


if __name__ == "__main__":
    run_quiz()
