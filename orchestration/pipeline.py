"""
This module orchestrates the fuzzing pipeline.
"""
import datetime
import json
import uuid

from attacks import mutator, attack_runner, base_prompt
from scoring import success_classifier

def _generate_reports(run_id, timestamp, responses, results, success_count, severity_counts):
    """Generates JSON and Markdown reports for the fuzzing run."""
    report_data = {
        "run_id": run_id,
        "timestamp": timestamp.isoformat(),
        "total_attacks": len(responses),
        "successes": success_count,
        "severity_breakdown": severity_counts,
        "results": results,
    }

    # Generate JSON report
    json_report_path = f"reports/run_{run_id}.json"
    with open(json_report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
    print(f"JSON report saved to {json_report_path}")

    # Generate Markdown report
    md_report_path = f"reports/run_{run_id}.md"
    with open(md_report_path, "w", encoding="utf-8") as f:
        f.write(f"# Fuzzing Report: {run_id}\n\n")
        f.write(f"**Timestamp:** {timestamp.isoformat()}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Total Attacks:** {len(responses)}\n")
        f.write(f"- **Successful Attacks:** {success_count}\n")
        f.write(f"- **Success Rate:** {success_count / len(responses) * 100:.2f}%\n\n")
        f.write("### Severity Breakdown\n\n")
        for severity, count in severity_counts.items():
            if severity != "NONE":
                f.write(f"- **{severity}:** {count}\n")

        f.write("\n## Detailed Results\n\n")
        for result in results:
            f.write(f"### Attack on {result['response']['model_name']}\n\n")
            f.write(f"**Prompt:** `{result['prompt']}`\n\n")
            f.write(f"**Response:** `{result['response']['response_text']}`\n\n")
            f.write(f"**Result:** {'Success' if result['classification']['success'] else 'Failure'} "
                    f"({result['classification']['severity']})\n\n")
            f.write("---\n\n")
    print(f"Markdown report saved to {md_report_path}")

def run_fuzzing_pipeline():
    """
    Orchestrates the entire fuzzing pipeline.
    """
    run_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now()

    print(f"Starting fuzzing pipeline for run ID: {run_id} at {timestamp.isoformat()}")

    # 1. Mutate the base prompt
    print("Step 1: Mutating base prompt...")
    base_prompt_text = base_prompt.BASE_ATTACK_PROMPT
    mutated_prompts = mutator.mutate_prompt(base_prompt_text, seed=42)
    print(f"Generated {len(mutated_prompts)} mutated prompts.")

    # 2. Run the attacks
    print("Step 2: Running attacks...")
    responses = attack_runner.run_attacks(mutated_prompts, run_id)
    print(f"Received {len(responses)} responses.")

    # 3. Score the results
    print("Step 3: Scoring responses...")
    results = []
    success_count = 0
    severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "NONE": 0}

    for i, response in enumerate(responses):
        classification = success_classifier.classify_response(response["response_text"])
        if classification["success"]:
            success_count += 1

        severity_str = classification["severity"].value
        severity_counts[severity_str] += 1

        results.append({
            "prompt": mutated_prompts[i // 2],  # Each prompt gets 2 mock responses
            "response": response,
            "classification": {
                "success": classification["success"],
                "severity": severity_str,
            },
        })
    print("Scoring complete.")

    # 4. Generate reports
    print("Step 4: Generating reports...")
    _generate_reports(run_id, timestamp, responses, results, success_count, severity_counts)

    return {
        "total_attacks": len(responses),
        "successes": success_count,
        "severity_breakdown": severity_counts,
    }
