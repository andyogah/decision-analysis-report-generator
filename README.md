# Decision Analysis Report Generator

Generates structured decision analysis reports (AoA, trade studies, business case analysis, cost-benefit analysis, options analysis) using an LLM and a Markdown template.

## Problem
Decision analysis documents are repetitive and time-consuming to draft and maintain consistently across projects and organizations. Teams often struggle with:
- Inconsistent report structures and quality
- Manual copy-paste from previous reports
- Time-consuming section writing and formatting
- Difficulty maintaining compliance with organizational standards

## Solution
A template-driven generator that:
- Accepts structured inputs (JSON) for mission/requirements/alternatives/criteria/costs/team
- Uses an LLM to fill a Markdown template aligned to DOE G 413.3-22 (generalized for broader use)
- Produces complete, auditable reports including a References section
- Ensures consistency across projects and teams

## Features
- **Multi-format support**: AoA, trade studies, business cases, cost-benefit analysis, options analysis
- **Dual LLM providers**: OpenAI and Azure OpenAI (configurable via environment)
- **Auto-generated references**: Reduces citation errors and improves traceability
- **Minimal setup**: Simple CLI with JSON input and Markdown output
- **Extensible**: Template-based architecture for easy customization

## Quick Start

1. **Clone and install**:
   ```bash
   git clone <repository-url>
   cd AoA
   pip install -r requirements.txt
   ```

2. **Set API key** (choose one):
   ```bash
   # OpenAI
   export OPENAI_API_KEY=your-key-here
   
   # OR Azure OpenAI
   export LLM_PROVIDER=azure
   export AZURE_OPENAI_API_KEY=your-key-here
   export AZURE_OPENAI_API_BASE=https://your-resource.openai.azure.com/
   export AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   ```

3. **Generate report**:
   ```bash
   python src/main.py
   ```
   
   Output: `aoa_report.md` in the project root

## Architecture

```
/c:/Users/path-to-your-project/AoA/
├── README.md                  # This file
├── LICENSE                    # MIT License
├── requirements.txt           # Python dependencies
├── .editorconfig             # Code formatting rules
├── aoa_templates/
│   └── aoa_template.md       # Markdown template with {{placeholders}}
├── data/
│   └── sample_input.json     # Example project data
└── src/
    ├── main.py               # Main orchestrator
    └── llm_client.py         # OpenAI/Azure client wrapper
```

### Data Flow
1. **Load**: Environment variables, template file, and input JSON
2. **Generate**: LLM creates content for each section using project context
3. **Merge**: Replace template placeholders with generated content
4. **Output**: Complete Markdown report ready for review/distribution

### Generated Sections
- Executive Summary, Scope, Mission Need
- Requirements & Assumptions, Alternatives
- Screening, Evaluation Criteria
- Cost & Schedule, Alternative Evaluation
- Conclusions, Team, Appendices, References

## Configuration

### Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_PROVIDER` | No | `openai` | Provider: `openai` or `azure` |
| `OPENAI_API_KEY` | Yes* | - | OpenAI API key |
| `AZURE_OPENAI_API_KEY` | Yes** | - | Azure OpenAI API key |
| `AZURE_OPENAI_API_BASE` | Yes** | - | Azure endpoint URL |
| `AZURE_OPENAI_API_VERSION` | No | `2023-05-15` | Azure API version |
| `AZURE_OPENAI_DEPLOYMENT` | Yes** | - | Azure deployment name |

*Required for OpenAI provider  
**Required for Azure provider

### Input JSON Schema
Your `data/sample_input.json` should contain:
```json
{
  "project_name": "string",
  "mission_need": "string",
  "requirements": ["string", "..."],
  "alternatives": [{"name": "string", "description": "string"}],
  "constraints": ["string", "..."],
  "evaluation_criteria": [{"criterion": "string", "weight": 0.0}],
  "cost_estimates": [{"alternative": "string", "cost": 0, "time": 0}],
  "team": [{"name": "string", "role": "string"}]
}
```

## Customization

### Template Modification
Edit `aoa_templates/aoa_template.md`:
- Add/remove sections
- Modify section headers
- Add new `{{placeholder}}` variables

### Input Extension
Add fields to your JSON and map them in `src/main.py`:
```python
sections = {
    "new_section": f"Generate content for: {data['new_field']}"
}
```

### Provider Switching
```bash
# Switch to Azure
export LLM_PROVIDER=azure
# Switch back to OpenAI  
export LLM_PROVIDER=openai
```

## Extending

### Near-term Enhancements
- **Web UI**: Flask/Streamlit interface for easier JSON input and template selection
- **Multiple formats**: YAML/CSV input support with schema conversion
- **CLI flags**: `--input`, `--output`, `--template`, `--model` parameters
- **Export options**: HTML/PDF output via Pandoc integration

### Advanced Features
- **Human-in-the-loop**: Review checklists, approval workflows, section locking
- **Quantitative integration**: CSV cost data import, NPV calculations, Monte Carlo risk analysis
- **References hardening**: User-provided source lists, numbered citations, metadata tracking
- **Schema validation**: JSON Schema enforcement with helpful error messages
- **Determinism controls**: Temperature/token controls, reproducible outputs

### Retrieval-Augmented Generation (RAG)
Enhance accuracy and reduce hallucinations:
- **Corpus**: Index organizational docs (policies, past reports, standards)
- **Retrieval**: Query-relevant chunks for each section
- **Grounding**: LLM uses retrieved content for citations and facts
- **Traceability**: Source metadata in generated references

Implementation approach:
```
/rag/
├── indexer.py      # Document chunking and embedding
├── retriever.py    # Similarity search and ranking  
└── corpus/         # Organizational knowledge base
```

## Design Decisions

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| Markdown templates | Portable, version-controllable, human-readable | Less rich than Word templates |
| JSON input schema | Structured, validatable, tool-friendly | More setup than free-form text |
| Environment config | Deployment flexibility, security | More setup steps |
| Single template file | Simplicity, easy customization | Less specialized than multiple templates |

## Outcomes & Benefits

✅ **Consistency**: Standardized structure across all reports  
✅ **Speed**: 10x faster than manual drafting  
✅ **Quality**: Comprehensive sections, proper formatting  
✅ **Compliance**: Built-in adherence to DOE G 413.3-22 structure  
✅ **Flexibility**: Works for government and commercial contexts  
✅ **Maintainability**: Version-controlled templates and inputs  

## Limitations & Mitigations

| Limitation | Impact | Mitigation (see Extending) |
|------------|---------|---------------------------|
| LLM hallucinations | Factual errors | RAG integration, human review workflows |
| Generic references | Poor traceability | References hardening with user sources |
| Limited quantitative analysis | Weak cost models | Quantitative integration with external tools |
| Output variability | Inconsistent results | Determinism controls, fixed prompts |

## Troubleshooting

### Common Issues
| Problem | Cause | Solution |
|---------|-------|---------|
| Empty output file | Missing API key | Set `OPENAI_API_KEY` or Azure variables |
| "Model not found" | Wrong Azure deployment | Check `AZURE_OPENAI_DEPLOYMENT` name |
| Sections show `{{placeholder}}` | Template/code mismatch | Verify placeholder names in template and `main.py` |
| Rate limit errors | Too many requests | Add delays, use smaller models, or upgrade plan |
| Unicode errors | File encoding | Ensure UTF-8 encoding in template/input files |

### Debug Steps
1. Verify environment variables: `echo $OPENAI_API_KEY`
2. Test API connection: `python -c "from src.llm_client import LLMClient; LLMClient().generate('test')"`
3. Check file paths and permissions
4. Review console output for specific error messages

## Contributing
Contributions welcome! Areas of interest:
- Additional templates (business case, SWOT analysis, etc.)
- Input format parsers (YAML, CSV, Excel)
- Output renderers (HTML, PDF, Word)
- Integration examples (CI/CD, SharePoint, etc.)

**Process**: Submit pull requests or open issues for enhancements/bugs.

## License
MIT License - see LICENSE file for details.

---
**Dependencies**: openai>=1.13.0, python-dotenv>=1.0.0  
**Python**: 3.8+ recommended  
**Tested**: OpenAI GPT-4, Azure OpenAI Service
