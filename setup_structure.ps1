# setup_structure.ps1
$root = "C:\Users\Muhammad Adeel Khan\geo-gap-compass"
New-Item -ItemType Directory -Path $root -Force | Out-Null
Set-Location $root

# create folders
New-Item frontend -ItemType Directory -Force
New-Item backend -ItemType Directory -Force
New-Item demo_data -ItemType Directory -Force

# frontend subfolders & files
New-Item -Path "$root\frontend\pages" -ItemType Directory -Force
New-Item -Path "$root\frontend\components" -ItemType Directory -Force
New-Item -Path "$root\frontend\utils" -ItemType Directory -Force
New-Item "$root\frontend\components\GapHeatmap.jsx" -ItemType File -Force
New-Item "$root\frontend\components\PromptTestLab.jsx" -ItemType File -Force
New-Item "$root\frontend\components\CompetitorPanel.jsx" -ItemType File -Force
New-Item "$root\frontend\components\InsightsPanel.jsx" -ItemType File -Force
New-Item "$root\frontend\utils\api.js" -ItemType File -Force

# backend subfolders & files
New-Item -Path "$root\backend\routes" -ItemType Directory -Force
New-Item -Path "$root\backend\utils" -ItemType Directory -Force
New-Item "$root\backend\app.py" -ItemType File -Force
New-Item "$root\backend\index.js" -ItemType File -Force
New-Item "$root\backend\db.json" -ItemType File -Force
New-Item "$root\backend\routes\prompts.py" -ItemType File -Force
New-Item "$root\backend\routes\citations.py" -ItemType File -Force
New-Item "$root\backend\routes\reimagine.py" -ItemType File -Force
New-Item "$root\backend\utils\ai_client.py" -ItemType File -Force
New-Item "$root\backend\utils\openai.js" -ItemType File -Force

# demo data
New-Item "$root\demo_data\fake_citations.json" -ItemType File -Force
New-Item "$root\demo_data\fake_time_series.json" -ItemType File -Force

# README
New-Item "$root\README.md" -ItemType File -Force

Write-Host "Structure created at $root"
