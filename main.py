"""
This is the main entry point for the adversarial LLM fuzzer.
"""
from orchestration import pipeline

def main():
    """
    The main entry point for the adversarial LLM fuzzer.
    """
    print("Starting Adversarial LLM Fuzzer...")
    summary = pipeline.run_fuzzing_pipeline()
    print("\n--- Fuzzing Run Summary ---")
    print(f"Total Attacks: {summary['total_attacks']}")
    print(f"Successful Attacks: {summary['successes']}")
    print("\nSeverity Breakdown:")
    for severity, count in summary['severity_breakdown'].items():
        if severity != "NONE":
            print(f"- {severity}: {count}")
    print("\nFuzzing complete. Check the 'reports/' directory for detailed logs.")

if __name__ == "__main__":
    main()
