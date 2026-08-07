## Phase 8: Post-Acceptance Deliverables

**Goal**: Maximize the impact of your accepted paper through presentation materials and community engagement.

### Step 8.1: Conference Poster

Most conferences require a poster session. Poster design principles:

| Element | Guideline |
|---------|-----------|
| **Size** | Check venue requirements (typically 24"x36" or A0 portrait/landscape) |
| **Content** | Title, authors, 1-sentence contribution, method figure, 2-3 key results, conclusion |
| **Flow** | Top-left to bottom-right (Z-pattern) or columnar |
| **Text** | Title readable at 3m, body at 1m. No full paragraphs â€” bullet points only. |
| **Figures** | Reuse paper figures at higher resolution. Enlarge key result. |

**Tools**: LaTeX (`beamerposter` package), PowerPoint/Keynote, Figma, Canva.

**Production**: Order 2+ weeks before the conference. Fabric posters are lighter for travel. Many conferences now support virtual/digital posters too.

### Step 8.2: Conference Talk / Spotlight

If awarded an oral or spotlight presentation:

| Talk Type | Duration | Content |
|-----------|----------|---------|
| **Spotlight** | 5 min | Problem, approach, one key result. Rehearse to exactly 5 minutes. |
| **Oral** | 15-20 min | Full story: problem, approach, key results, ablations, limitations. |
| **Workshop talk** | 10-15 min | Adapt based on workshop audience â€” may need more background. |

**Slide design rules:**
- One idea per slide
- Minimize text â€” speak the details, don't project them
- Animate key figures to build understanding step-by-step
- Include a "takeaway" slide at the end (single sentence contribution)
- Prepare backup slides for anticipated questions

### Step 8.3: Blog Post / Social Media

An accessible summary significantly increases impact:

- **Twitter/X thread**: 5-8 tweets. Lead with the result, not the method. Include Figure 1 and key result figure.
- **Blog post**: 800-1500 words. Written for ML practitioners, not reviewers. Skip formalism, emphasize intuition and practical implications.
- **Project page**: HTML page with abstract, figures, demo, code link, BibTeX. Use GitHub Pages.

**Timing**: Post within 1-2 days of paper appearing on proceedings or arXiv camera-ready.

---

## Workshop & Short Papers

Workshop papers and short papers (e.g., ACL short papers, Findings papers) follow the same pipeline but with different constraints and expectations.

### Workshop Papers

| Property | Workshop | Main Conference |
|----------|----------|-----------------|
| **Page limit** | 4-6 pages (typically) | 7-9 pages |
| **Review standard** | Lower bar for completeness | Must be complete, thorough |
| **Review process** | Usually single-blind or light review | Double-blind, rigorous |
| **What's valued** | Interesting ideas, preliminary results, position pieces | Complete empirical story with strong baselines |
| **arXiv** | Post anytime | Timing matters (see arXiv strategy) |
| **Contribution bar** | Novel direction, interesting negative result, work-in-progress | Significant advance with strong evidence |

**When to target a workshop:**
- Early-stage idea you want feedback on before a full paper
- Negative result that doesn't justify 8+ pages
- Position piece or opinion on a timely topic
- Replication study or reproducibility report

### ACL Short Papers & Findings

ACL venues have distinct submission types:

| Type | Pages | What's Expected |
|------|-------|-----------------|
| **Long paper** | 8 | Complete study, strong baselines, ablations |
| **Short paper** | 4 | Focused contribution: one clear point with evidence |
| **Findings** | 8 | Solid work that narrowly missed main conference |

**Short paper strategy**: Pick ONE claim and support it thoroughly. Don't try to compress a long paper into 4 pages â€” write a different, more focused paper.

---

## Paper Types Beyond Empirical ML

The main pipeline above targets empirical ML papers. Other paper types require different structures and evidence standards. See [references/paper-types.md](references/paper-types.md) for detailed guidance on each type.

### Theory Papers

**Structure**: Introduction â†’ Preliminaries (definitions, notation) â†’ Main Results (theorems) â†’ Proof Sketches â†’ Discussion â†’ Full Proofs (appendix)

**Key differences from empirical papers:**
- Contribution is a theorem, bound, or impossibility result â€” not experimental numbers
- Methods section replaced by "Preliminaries" and "Main Results"
- Proofs are the evidence, not experiments (though empirical validation of theory is welcome)
- Proof sketches in main text, full proofs in appendix is standard practice
- Experimental section is optional but strengthens the paper if it validates theoretical predictions

**Proof writing principles:**
- State theorems formally with all assumptions explicit
- Provide intuition before formal proof ("The key insight is...")
- Proof sketches should convey the main idea in 0.5-1 page
- Use `\begin{proof}...\end{proof}` environments
- Number assumptions and reference them in theorems: "Under Assumptions 1-3, ..."

### Survey / Tutorial Papers

**Structure**: Introduction â†’ Taxonomy / Organization â†’ Detailed Coverage â†’ Open Problems â†’ Conclusion

**Key differences:**
- Contribution is the organization, synthesis, and identification of open problems â€” not new methods
- Must be comprehensive within scope (reviewers will check for missing references)
- Requires a clear taxonomy or organizational framework
- Value comes from connections between works that individual papers don't make
- Best venues: TMLR (survey track), JMLR, Foundations and Trends in ML, ACM Computing Surveys

### Benchmark Papers

**Structure**: Introduction â†’ Task Definition â†’ Dataset Construction â†’ Baseline Evaluation â†’ Analysis â†’ Intended Use & Limitations

**Key differences:**
- Contribution is the benchmark itself â€” it must fill a genuine evaluation gap
- Dataset documentation is mandatory, not optional (see Datasheets, Step 5.11)
- Must demonstrate the benchmark is challenging (baselines don't saturate it)
- Must demonstrate the benchmark measures what you claim it measures (construct validity)
- Best venues: NeurIPS Datasets & Benchmarks track, ACL (resource papers), LREC-COLING

### Position Papers

**Structure**: Introduction â†’ Background â†’ Thesis / Argument â†’ Supporting Evidence â†’ Counterarguments â†’ Implications

**Key differences:**
- Contribution is an argument, not a result
- Must engage seriously with counterarguments
- Evidence can be empirical, theoretical, or logical analysis
- Best venues: ICML (position track), workshops, TMLR

---

