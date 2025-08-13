"""Decision analysis report generator: orchestrates LLM-driven template filling."""

import json
import os
from dotenv import load_dotenv  # added
from llm_client import LLMClient

def load_template(path):
    """Read and return the template file contents located at 'path'."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_input(path):
    """Load and return structured input JSON from 'path'."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def fill_template(template, data, llm):
    """Generate each report section with the LLM and merge into the template."""
    sections = {
        "executive_summary": "Write a 1-paragraph executive summary for this AoA.",
        "scope": "Describe the scope of this AoA.",
        "introduction_and_mission_need": f"Summarize the mission need: {data['mission_need']}",
        "requirements_and_assumptions": f"List the requirements: {data['requirements']}. List the constraints: {data['constraints']}.",
        "alternatives": f"Describe these alternatives: {data['alternatives']}",
        "screening": "Describe the initial screening of alternatives.",
        "evaluation_criteria": f"List and explain these evaluation criteria: {data['evaluation_criteria']}",
        "cost_and_schedule": f"Summarize cost and schedule estimates: {data['cost_estimates']}",
        "alternative_evaluation": "Evaluate and rank the alternatives based on the criteria, cost, and risk.",
        "conclusions": "Provide a conclusion and recommendation.",
        "team": f"List the team members and their roles: {data['team']}",
        "appendices": "Add any relevant appendices or notes.",
        "references": "List any references, sources, or documents used in this analysis, including standards, templates, or guidance such as DOE G 413.3-22."
    }
    filled = template.replace("{{project_name}}", data.get("project_name", ""))
    for key, prompt in sections.items():
        context = f"Project data: {json.dumps(data, indent=2)}\n\n"
        full_prompt = context + prompt
        print(f"Generating section: {key} ...")
        section_text = llm.generate(full_prompt)
        filled = filled.replace(f"{{{{{key}}}}}", section_text)
    return filled

def main():
    """Entry point to read inputs, generate the report, and write output."""
    load_dotenv()  # added
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, "aoa_templates", "aoa_template.md")
    input_path = os.path.join(base_dir, "data", "sample_input.json")
    output_path = os.path.join(base_dir, "aoa_report.md")

    template = load_template(template_path)
    data = load_input(input_path)
    llm = LLMClient()

    report = fill_template(template, data, llm)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"AoA report generated at {output_path}")

if __name__ == "__main__":
    main()
