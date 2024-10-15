import argparse
import os


def parse_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        type=str,
        help="Filepath to the grammar used for \
                code generation.",
    )

    parser.add_argument(
        "--output_file", type=str, help="Path to the generated python file."
    )

    return parser.parse_args()


def generate_ast(grammar: str):
    """Generates classes for each expression type."""

    output = f"class ExpressionBase:\n    pass\n\n"

    for expression in grammar.splitlines():
        rule = expression.split()
        name = rule[0]

        output += f"@dataclass\nclass {name}Expr(ExpressionBase):\n"
        output += f'    """Data class for expressions of type {name}"""\n'

        for var in rule[1:]:
            annotation = "object" if var == "expr" else "Token"
            output += f"    this.{var}: {annotation} = {var}\n"
        output += "\n"
    return output


def main():
    """Main for the expression class generator"""
    args = parse_args()
    if args.input_file:
        if os.path.isfile(args.input_file):
            with open(args.input_file, "r", encoding="utf-8") as file:
                grammar = file.read()
                ast = generate_ast(grammar)
            with open(args.output_file, "w", encoding="utf-8") as output_file:
                output_file.write(ast)
        else:
            raise ValueError(f"Provided file {args.filepath} is not a file.")
    else:
        run_prompt()


if __name__ == "__main__":
    main()
