import os
import logging
from benchmark_collection.utils.openai_utils import GPTClient

class Refiner:
    def __init__(self, research_field, instance_id, gpt_model='gpt-4o-2024-05-13'):
        self.project_dir = f"{research_field}/target_sections/{instance_id}"
        self.gpt_client = GPTClient(model=gpt_model)
        self.section_mapping = {
            "introduction": "introduction.tex",
            "related work": "related_work.tex",
            "methodology": "methodology.tex",
            "method": "methodology.tex",
            "proposed method": "methodology.tex",
            "experiments": "experiments.tex",
            "experiment": "experiments.tex",
            "conclusion": "conclusion.tex",
            "abstract": "abstract.tex"
        }

    async def refine_paper(self, review_report):
        recommendations = review_report.get("specific_recommendations_for_revision", [])

        for rec in recommendations:
            section_name = rec.get("section", "").lower()
            comment = rec.get("comment", "")

            target_file = None
            # Try to match key in section name
            for key, filename in self.section_mapping.items():
                if key in section_name:
                    target_file = filename
                    break

            # Fallback: try to find a file that matches the section name directly
            if not target_file and os.path.exists(self.project_dir):
                for filename in os.listdir(self.project_dir):
                    if filename.endswith(".tex") and filename.replace(".tex", "").lower() in section_name:
                        target_file = filename
                        break

            if target_file:
                await self._revise_section(target_file, comment)
            else:
                logging.warning(f"Could not find target file for section: {section_name}")

    async def _revise_section(self, filename, comment):
        filepath = os.path.join(self.project_dir, filename)
        if not os.path.exists(filepath):
            logging.warning(f"File not found: {filepath}")
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        prompt = f"""You are an expert academic writer.
You are refining a section of a paper based on a reviewer's comment.

Current Content ({filename}):
{content}

Reviewer's Comment:
{comment}

Task:
Rewrite the content to address the reviewer's comment.
Maintain the LaTeX format.
Do not remove valid technical content unless asked to.
Improve clarity and flow.
Ensure the output is valid LaTeX.

Output ONLY the revised LaTeX content.
"""
        response = await self.gpt_client.chat(prompt=prompt)

        # Clean up code blocks if present
        if response.startswith("```latex"):
            response = response.split("```latex")[1]
            if response.endswith("```"):
                response = response.rsplit("```", 1)[0]
        elif response.startswith("```tex"):
             response = response.split("```tex")[1]
             if response.endswith("```"):
                response = response.rsplit("```", 1)[0]
        elif response.startswith("```"):
            response = response.split("```")[1]
            if response.endswith("```"):
                response = response.rsplit("```", 1)[0]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.strip())

        logging.info(f"Revised {filename} based on feedback.")
