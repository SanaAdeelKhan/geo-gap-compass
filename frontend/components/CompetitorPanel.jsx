"use client";
import { useState } from "react";
import { analyzeCompetitors } from "@/utils/api";

export default function CompetitorPanel() {
  const [brand, setBrand] = useState("Nike");
  const [competitors, setCompetitors] = useState("Adidas, Puma, Under Armour");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const competitorList = competitors
        .split(",")
        .map(c => c.trim())
        .filter(c => c.length > 0);

      if (!brand.trim() || competitorList.length === 0) {
        setError("Please enter brand and at least one competitor");
        setLoading(false);
        return;
      }

      const res = await analyzeCompetitors(brand, competitorList);
      setData(res);
    } catch (err) {
      setError(err.message || "Failed to analyze competitors");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Competitor Analysis</h1>

      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Brand
            </label>
            <input
              type="text"
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={brand}
              onChange={(e) => setBrand(e.target.value)}
              placeholder="e.g., Nike"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Competitors (comma-separated)
            </label>
            <input
              type="text"
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={competitors}
              onChange={(e) => setCompetitors(e.target.value)}
              placeholder="e.g., Adidas, Puma, Under Armour"
            />
          </div>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded font-medium transition"
        >
          {loading ? "Analyzing..." : "Analyze Competitors"}
        </button>
      </div>

      {data && (
        <div className="space-y-6">
          {/* Summary */}
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <h2 className="font-semibold text-lg mb-2">
              Competitive Landscape for {data.brand}
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Competitors:</span>
                <p className="font-medium">{data.competitors.length}</p>
              </div>
              <div>
                <span className="text-gray-600">Top Competitor:</span>
                <p className="font-medium">
                  {data.competitors[0]?.name || "N/A"}
                </p>
              </div>
              <div>
                <span className="text-gray-600">Tokens Used:</span>
                <p className="font-medium">{data.tokens_used || "0"}</p>
              </div>
              <div>
                <span className="text-gray-600">Using OpenAI:</span>
                <p className="font-medium">{data.using_openai ? "Yes" : "Mock"}</p>
              </div>
            </div>
          </div>

          {/* Competitor Scores */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="font-semibold text-lg mb-4">Competitor Scores</h3>
            <div className="space-y-3">
              {data.competitors.map((comp, idx) => (
                <div key={idx} className="flex items-center justify-between">
                  <span className="font-medium">{comp.name}</span>
                  <div className="flex items-center gap-3">
                    <div className="w-48 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all"
                        style={{ width: `${comp.score}%` }}
                      />
                    </div>
                    <span className="font-semibold w-12 text-right">
                      {comp.score}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Detailed Analysis */}
          {data.detailed_analysis && (
            <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
              <h3 className="font-semibold text-lg mb-3">Detailed Analysis</h3>
              <p className="text-gray-700 whitespace-pre-wrap text-sm leading-relaxed">
                {data.detailed_analysis}
              </p>
            </div>
          )}
        </div>
      )}

      {loading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      )}
    </div>
  );
}