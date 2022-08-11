import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'radar-pipeline/')
from radarpipeline import radarpipeline

if __name__ == "__main__":
    radarpipeline.run()