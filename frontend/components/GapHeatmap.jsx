"use client";
import React from "react";

export default function GapHeatmap({ data, brand }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white p-8 rounded-lg shadow-md text-center">
        <p className="text-gray-500">No data available. Generate a heatmap to see results.</p>
      </div>
    );
  }

  const getColor = (score) => {
    if (score >= 70) return "bg-green-500";
    if (score >= 50) return "bg-yellow-400";
    if (score >= 30) return "bg-orange-400";
    return "bg-red-500";
  };

  const getGapColor = (gap) => {
    if (gap >= 40) return "text-red-600";
    if (gap >= 20) return "text-orange-600";
    if (gap >= 0) return "text-yellow-600";
    return "text-green-600";
  };

  const getPriority = (gap) => {
    if (gap >= 40) return { label: "High", color: "bg-red-100 text-red-800" };
    if (gap >= 20) return { label: "Medium", color: "bg-yellow-100 text-yellow-800" };
    return { label: "Low", color: "bg-green-100 text-green-800" };
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="p-6">
        <h3 className="text-xl font-semibold mb-4">
          Citation Gap Heatmap for {brand}
        </h3>

        {/* Legend */}
        <div className="flex flex-wrap gap-4 mb-6 p-4 bg-gray-50 rounded">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-green-500 rounded"></div>
            <span className="text-sm">70-100% (High)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-yellow-400 rounded"></div>
            <span className="text-sm">50-69% (Moderate)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-orange-400 rounded"></div>
            <span className="text-sm">30-49% (Low)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-red-500 rounded"></div>
            <span className="text-sm">0-29% (Critical)</span>
          </div>
        </div>

        {/* Desktop Table */}
        <div className="hidden md:block overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold">
                  Content Type
                </th>
                <th className="px-4 py-3 text-center text-sm font-semibold">
                  Your Brand
                </th>
                <th className="px-4 py-3 text-center text-sm font-semibold">
                  Top Competitor
                </th>
                <th className="px-4 py-3 text-center text-sm font-semibold">
                  Gap
                </th>
                <th className="px-4 py-3 text-center text-sm font-semibold">
                  Priority
                </th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => {
                const gap = row.competitorScore - row.yourBrandScore;
                const priority = getPriority(gap);

                return (
                  <tr key={idx} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium capitalize">
                      {row.promptType.replace(/-/g, " ")}
                    </td>
                    <td className="px-4 py-3 text-center">
                      <div
                        className={`inline-flex items-center justify-center w-16 h-10 rounded font-semibold text-white ${getColor(
                          row.yourBrandScore
                        )}`}
                      >
                        {row.yourBrandScore}%
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <div
                        className={`inline-flex items-center justify-center w-16 h-10 rounded font-semibold text-white ${getColor(
                          row.competitorScore
                        )}`}
                      >
                        {row.competitorScore}%
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className={`font-semibold ${getGapColor(gap)}`}>
                        {gap > 0 ? "+" : ""}{gap}%
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${priority.color}`}>
                        {priority.label}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Mobile Cards */}
        <div className="md:hidden space-y-4">
          {data.map((row, idx) => {
            const gap = row.competitorScore - row.yourBrandScore;
            const priority = getPriority(gap);

            return (
              <div key={idx} className="p-4 border rounded-lg bg-gray-50">
                <div className="flex justify-between items-center mb-3">
                  <h4 className="font-semibold capitalize">
                    {row.promptType.replace(/-/g, " ")}
                  </h4>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${priority.color}`}>
                    {priority.label}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-2 text-center text-sm">
                  <div>
                    <p className="text-gray-600 text-xs mb-1">Your Brand</p>
                    <div className={`py-2 rounded font-semibold text-white ${getColor(row.yourBrandScore)}`}>
                      {row.yourBrandScore}%
                    </div>
                  </div>
                  <div>
                    <p className="text-gray-600 text-xs mb-1">Competitor</p>
                    <div className={`py-2 rounded font-semibold text-white ${getColor(row.competitorScore)}`}>
                      {row.competitorScore}%
                    </div>
                  </div>
                  <div>
                    <p className="text-gray-600 text-xs mb-1">Gap</p>
                    <div className={`py-2 rounded font-semibold ${getGapColor(gap)}`}>
                      {gap > 0 ? "+" : ""}{gap}%
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}