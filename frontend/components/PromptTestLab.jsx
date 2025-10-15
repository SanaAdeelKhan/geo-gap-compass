"use client";
// FILE: components/PromptTestLab.jsx (Enhanced + Global Persistence)
// ============================================================================

import { useState } from "react";
import { testPrompts } from "@/utils/api";
import usePromptStore from "@/store/usePromptStore"; // ✅ NEW import

export default function PromptTestLab() {
  const [brand, setBrand] = useState("Nike");
  const [customPrompts, setCustomPrompts] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState("auto"); // auto or custom

  // ✅ Global store (auto-persistent)
  const { results, setResults, clearResults } = usePromptStore();

  const handleRunTest = async () => {
    setLoading(true);
    setError(null);

    try {
      let promptVariations = null;
      if (mode === "custom" && customPrompts.trim()) {
        promptVariations = customPrompts
          .split("\n")
          .map((p) => p.trim())
          .filter((p) => p.length > 0);
      }

      const data = await testPrompts(brand, promptVariations);
      setResults(data); // ✅ Save globally
    } catch (err) {
      setError(err.message);
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    clearResults(); // ✅ Clears from global + localStorage
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4">Prompt Testing Lab</h3>

      {/* Mode Selection */}
      <div className="mb-4">
        <div className="flex gap-2">
          <button
            onClick={() => setMode("auto")}
            className={`px-4 py-2 rounded font-medium transition ${
              mode === "auto"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            Auto-Generate Prompts
          </button>
          <button
            onClick={() => setMode("custom")}
            className={`px-4 py-2 rounded font-medium transition ${
              mode === "custom"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            Custom Prompts
          </button>
        </div>
      </div>

      {/* Brand Input */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Brand Name</label>
        <input
          className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={brand}
          onChange={(e) => setBrand(e.target.value)}
          placeholder="Enter brand name (e.g., Nike)"
        />
      </div>

      {/* Custom Prompts Input */}
      {mode === "custom" && (
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">
            Custom Prompts (one per line)
          </label>
          <textarea
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={6}
            value={customPrompts}
            onChange={(e) => setCustomPrompts(e.target.value)}
            placeholder={`What are Nike's latest innovations?\nHow does Nike compare to Adidas?\nBest Nike running shoes for marathon`}
          />
        </div>
      )}

      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Run Button */}
      <button
        onClick={handleRunTest}
        disabled={loading || !brand.trim()}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded font-medium transition"
      >
        {loading ? "Running Tests..." : "Run Prompt Tests"}
      </button>

      {/* Clear Report Button (manual) */}
      {results && (
        <div className="mt-3 flex justify-end">
          <button
            onClick={handleClear}
            className="text-sm px-3 py-1 rounded bg-red-100 text-red-700 hover:bg-red-200"
          >
            🧹 Clear Report
          </button>
        </div>
      )}

      {/* Results Display (unchanged UI) */}
      {results && (
        <div className="mt-6">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200 mb-4">
            <h4 className="font-semibold mb-2">Test Summary for {results.brand}</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Prompts Tested:</span>
                <p className="font-medium">{results.summary?.total_prompts || 0}</p>
              </div>
              <div>
                <span className="text-gray-600">Total Citations:</span>
                <p className="font-medium">{results.summary?.total_citations || 0}</p>
              </div>
              <div>
                <span className="text-gray-600">Tokens Used:</span>
                <p className="font-medium">{results.summary?.total_tokens_used || 0}</p>
              </div>
              <div>
                <span className="text-gray-600">Using OpenAI:</span>
                <p className="font-medium">{results.summary?.using_openai ? "Yes" : "Mock"}</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h4 className="font-semibold text-lg">Results</h4>
            {results.results?.map((result, idx) => (
              <div key={idx} className="p-4 border rounded-lg hover:shadow-md transition">
                <div className="mb-2">
                  <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded font-medium">
                    Prompt #{idx + 1}
                  </span>
                </div>
                <p className="text-sm italic text-gray-700 mb-3">{result.prompt}</p>

                {result.error ? (
                  <div className="text-red-600 text-sm">Error: {result.error}</div>
                ) : (
                  <>
                    <div className="text-sm text-gray-800 mb-3 line-clamp-3">{result.response}</div>
                    <div className="flex flex-wrap gap-2 items-center text-xs">
                      <span className="text-gray-600">Citations:</span>
                      {result.citations && result.citations.length > 0 ? (
                        result.citations.map((url, urlIdx) => (
                          <a
                            key={urlIdx}
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline"
                          >
                            {new URL(url).hostname}
                          </a>
                        ))
                      ) : (
                        <span className="text-gray-500">No citations found</span>
                      )}
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {loading && (
        <div className="flex justify-center py-8">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
        </div>
      )}
    </div>
  );
}
