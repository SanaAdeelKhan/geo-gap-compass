"use client";
// FILE: app/dashboard/prompts/page.jsx
// =============================================================================

import { useState } from "react";
import PromptTestLab from "@/components/PromptTestLab";

export default function PromptsPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">Prompt Testing Lab</h1>
        <p className="text-gray-600 mb-6">
          Test your brand visibility across different AI prompt types
        </p>
        <PromptTestLab />
      </div>
    </div>
  );
}