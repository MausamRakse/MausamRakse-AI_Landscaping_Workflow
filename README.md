# MausamRakse-AI_Landscaping_Workflow
An AI-powered system that analyzes user-provided plot images and metadata to automatically generate landscaping plans, plant suggestions, and annotated visuals.

🚀 Overview

This workflow accepts:

2+ plot images

Plot details (location, size, owner name)

Preferred theme (Modern, Traditional, Old-Fashioned)

Using LLMs (Gemini) + vision analysis + LangChain/LangGraph orchestration, it produces:

Annotated images with plant/decor placements

A structured landscaping plan (plant list, layout zones, theme alignment)

Exportable JSON/CSV for external use

🔧 How It Works (Short)

Input Collection – User uploads images + plot details.

Vision Analysis – Detects lawn, walls, shade, hardscape, usable areas.

Context Enrichment – Adds climate/plant data based on location.

LLM Design Planning – Gemini generates a theme-aligned landscape plan.

Graph Workflow (LangGraph) – Parallel tasks (vision + climate + design validation).

Output Generation – Final plan + annotated images + structured JSON.

🧠 Tech Stack

Gemini API (LLM design generation)

Vision models (segmentation / detection)

LangChain (prompt orchestration, tools)

LangGraph (workflow nodes, branching, validation)

Local plant/climate knowledge base

📦 Inputs

Plot images (2+)

Plot size

Location (for climate zones)

Design theme

Optional constraints (budget, maintenance level)

📤 Outputs

Annotated images

Landscaping plan (zones, plants, spacing, care)

JSON export

🔑 Environment Variables

GEMINI_API_KEY

VISION_API_KEY (if using external vision API)

📌 Roadmap

Better plant database

3D reconstruction for spatial accuracy

User feedback loop for iterative design

📄 License

Add your preferred license (MIT recommended).
