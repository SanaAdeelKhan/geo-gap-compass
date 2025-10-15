"use client";
import { useState } from "react";
import { getGapHeatmap } from "@/utils/api";
import GapHeatmap from "@/components/GapHeatmap";

export default function HeatmapPage() {
  const [brand, setBrand] = useState("Nike");
  const [topics, setTopics] = useState(
    "how-to,comparison,reviews,tutorials,pricing,alternatives"
  );
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const topicList = topics.split(",").map(t => t.trim()).filter(t => t);
      
      if (!brand || topicList.length === 0) {
        throw new Error("Brand and topics are required");
      }

      const result = await getGapHeatmap(brand, topicList);
      setData(result);
    } catch (err) {
      setError(err.message);
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2">Gap Heatmap Analysis</h1>
          <p className="text-gray-600">
            Discover citation gaps across different content types
          </p>
        </div>

        {/* Input Controls */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Brand Name
              </label>
              <input
                type="text"
                value={brand}
                onChange={(e) => setBrand(e.target.value)}
                className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Nike"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">
                Topics (comma-separated)
              </label>
              <input
                type="text"
                value={topics}
                onChange={(e) => setTopics(e.target.value)}
                className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., how-to, comparison, reviews"
              />
            </div>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded transition"
          >
            {loading ? "Generating..." : "Generate Heatmap"}
          </button>
        </div>

        {/* Heatmap Display */}
        {data && <GapHeatmap data={data.data} brand={data.brand} />}

        {/* AI Recommendations */}
        {data?.recommendations && (
          <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500 mt-6">
            <h3 className="font-semibold text-lg mb-3">AI Recommendations</h3>
            <div className="prose prose-sm max-w-none">
              <p className="text-gray-700 whitespace-pre-wrap">
                {data.recommendations}
              </p>
            </div>
            {data.tokens_used && (
              <p className="text-xs text-gray-500 mt-4">
                Tokens used: {data.tokens_used} | Using OpenAI: {data.using_openai ? "Yes" : "No"}
              </p>
            )}
          </div>
        )}

        {loading && (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        )}
      </div>
    </div>
  );
}