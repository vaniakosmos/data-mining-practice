from utils_pack.measurments import *


def print_title(title: str, length=89):
    half = (length - len(title) - 2) // 2
    corrector = 1 if len(title) % 2 == 0 else 0
    print(f"{'#'*length}")
    print(f"{'#'*half} {title} {'#'*(half + corrector)}")
    print(f"{'#'*length}\n")


def print_header(header: str, length=88):
    print(f"+{'-'*length}\n"
          f"| {header}\n"
          f"+{'-'*(length-1)}\n")


def print_results(confusion_matrix):
    print("Confusion Matrix:")
    print("\n".join(map(str, confusion_matrix)))
    print(f"Macro f1-score: {macro_f1_score(confusion_matrix)}")
    print(f"Micro f1-score: {micro_f1_score(confusion_matrix)}")
    print()
