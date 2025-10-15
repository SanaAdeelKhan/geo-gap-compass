"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, Globe, Database, BarChart3, AlertTriangle } from "lucide-react";
import { getDomainInsights } from "@/utils/api";

export default function DomainInsights() {
  const [brand, setBrand] = useState("Nike");
  const [domains, setDomains] = useState("nike.com, sneakernews.com, complex.com");
  const [analysisType, setAnalysisType] = useState("comprehensive");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const domainArray = domains
        .split(",")
        .map((d) => d.trim())
        .filter((d) => d.length > 0);

      if (domainArray.length === 0) {
        setError("Please enter at least one domain.");
        setLoading(false);
        return;
      }

      if (!brand.trim()) {
        setError("Please enter a brand name.");
        setLoading(false);
        return;
      }

      const res = await getDomainInsights(brand, domainArray, analysisType);

      setResult({
        brand: res.brand,
        domains: res.domains,
        analysis: res.full_analysis,
        sources: res.data_sources,
        tokensUsed: res.tokens_used,
        usingOpenAI: res.using_openai,
        isMock: res.is_mock,
      });
    } catch (err) {
      console.error("Error:", err);
      setError(err.message || "Failed to fetch domain insights");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* HEADER */}
      <motion.h1
        className="text-3xl font-bold text-center text-blue-600"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        🌐 GEO Gap Compass — Domain Insights
      </motion.h1>

      {/* INPUT FORM */}
      <Card className="shadow-lg border border-blue-100">
        <CardHeader>
          <CardTitle className="text-blue-700">Analyze Brand Domains</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input
              type="text"
              placeholder="Brand Name"
              value={brand}
              onChange={(e) => setBrand(e.target.value)}
              className="border rounded-xl p-2 w-full focus:ring-2 focus:ring-blue-400"
            />
            <input
              type="text"
              placeholder="Domains (comma-separated)"
              value={domains}
              onChange={(e) => setDomains(e.target.value)}
              className="border rounded-xl p-2 w-full focus:ring-2 focus:ring-blue-400"
            />
            <select
              value={analysisType}
              onChange={(e) => setAnalysisType(e.target.value)}
              className="border rounded-xl p-2 w-full focus:ring-2 focus:ring-blue-400"
            >
              <option value="comprehensive">Comprehensive</option>
              <option value="seo">SEO Focused</option>
              <option value="authority">Authority Analysis</option>
              <option value="trend">Trend Analysis</option>
            </select>
          </div>

          {error && (
            <div className="flex items-center gap-2 bg-red-100 border border-red-400 text-red-700 rounded p-3 text-sm">
              <AlertTriangle size={16} />
              {error}
            </div>
          )}

          <Button
            onClick={handleAnalyze}
            className="bg-blue-600 text-white hover:bg-blue-700 w-full mt-2"
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin mr-2" /> Running Analysis...
              </>
            ) : (
              "Analyze Domains"
            )}
          </Button>
        </CardContent>
      </Card>

      {/* LOADING STATE */}
      {loading && (
        <div className="flex justify-center items-center py-10">
          <Loader2 className="animate-spin text-blue-600 h-10 w-10" />
        </div>
      )}

      {/* RESULTS SECTION */}
      {result && !loading && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="space-y-6"
        >
          {/* SUMMARY CARD */}
          <Card className="border border-blue-100 shadow-sm">
            <CardHeader className="flex items-center space-x-2">
              <Globe className="text-blue-600" />
              <CardTitle>{result.brand} — Domain Analysis Summary</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-700">
              <div>
                <p className="font-medium">Domains Analyzed</p>
                <p>{Object.keys(result.domains || {}).length}</p>
              </div>
              <div>
                <p className="font-medium">Using OpenAI</p>
                <p>{result.usingOpenAI ? "Yes" : "Mock Data"}</p>
              </div>
              <div>
                <p className="font-medium">Tokens Used</p>
                <p>{result.tokensUsed || 0}</p>
              </div>
              <div>
                <p className="font-medium">Data Sources</p>
                <p className="text-xs">
                  {result.sources?.basic_info} + {result.sources?.analysis}
                </p>
              </div>
            </CardContent>
          </Card>

          {/* DOMAIN DETAILS */}
          <Card className="border border-blue-100 shadow-sm">
            <CardHeader className="flex items-center space-x-2">
              <Database className="text-blue-600" />
              <CardTitle>Domain Details</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(result.domains || {}).map(([domain, info]) => (
                <div
                  key={domain}
                  className="p-4 border rounded-lg shadow hover:shadow-lg transition bg-white"
                >
                  <h4 className="font-semibold text-base mb-2 truncate">{info.title || domain}</h4>
                  <p className="text-sm text-gray-600 mb-3">{info.description}</p>

                  {info.image && (
                    <img
                      src={info.image}
                      alt={domain}
                      className="w-full h-32 object-cover rounded mb-3"
                    />
                  )}

                  <div className="space-y-2 text-xs mb-3">
                    {info.visibility_score !== undefined && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Visibility:</span>
                        <span className="font-medium">{info.visibility_score}%</span>
                      </div>
                    )}
                    {info.mentions_in_analysis !== undefined && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Mentions:</span>
                        <span className="font-medium">{info.mentions_in_analysis}</span>
                      </div>
                    )}
                    {info.relevance_score !== undefined && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Relevance:</span>
                        <span className="font-medium">{info.relevance_score}%</span>
                      </div>
                    )}
                  </div>

                  <div className="flex items-center justify-between pt-3 border-t">
                    <div className="flex gap-1">
                      {info.authority_indicators && (
                        <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                          Authoritative
                        </span>
                      )}
                      {info.recommended && (
                        <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                          Recommended
                        </span>
                      )}
                    </div>
                  </div>

                  <p className="text-xs text-gray-400 mt-2">
                    Source: {info.source || "Unknown"}
                  </p>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* AI ANALYSIS */}
          {result.analysis && (
            <Card className="border border-blue-100 shadow-sm">
              <CardHeader className="flex items-center space-x-2">
                <BarChart3 className="text-blue-600" />
                <CardTitle>AI Analysis Summary</CardTitle>
              </CardHeader>
              <CardContent className="text-gray-700 whitespace-pre-wrap text-sm leading-relaxed">
                {result.analysis}
              </CardContent>
            </Card>
          )}
        </motion.div>
      )}
    </div>
  );
}
