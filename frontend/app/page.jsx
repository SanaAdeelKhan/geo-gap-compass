"use client";
// FILE: app/page.jsx (Landing/Home Page)
// =============================================================================

import { useRouter } from "next/navigation";
import { TrendingUp, Users, Globe, BarChart3, ArrowRight } from "lucide-react";

export default function HomePage() {
  const router = useRouter();

  const features = [
    {
      icon: BarChart3,
      title: "Prompt Testing",
      description: "Test brand visibility across multiple AI prompt variations"
    },
    {
      icon: TrendingUp,
      title: "Gap Analysis",
      description: "Identify citation gaps in AI-generated content"
    },
    {
      icon: Users,
      title: "Competitor Tracking",
      description: "Compare your brand presence with competitors"
    },
    {
      icon: Globe,
      title: "Domain Insights",
      description: "Analyze domain authority and relevance"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            GEO Gap Compass
          </h1>
          <p className="text-xl md:text-2xl text-gray-700 mb-8">
            Discover where your brand is missing in AI-generated answers
          </p>
          <p className="text-lg text-gray-600 mb-10 max-w-3xl mx-auto">
            Track, analyze, and optimize your brand's visibility across AI assistants 
            like ChatGPT. It's Google Analytics for Generative AI.
          </p>
          <button
            onClick={() => router.push("/dashboard")}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-4 rounded-lg text-lg flex items-center gap-2 mx-auto transition"
          >
            Go to Dashboard
            <ArrowRight size={20} />
          </button>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
          {features.map((feature, idx) => (
            <div
              key={idx}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition"
            >
              <feature.icon className="text-blue-600 mb-4" size={32} />
              <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
              <p className="text-gray-600 text-sm">{feature.description}</p>
            </div>
          ))}
        </div>

        {/* Value Proposition */}
        <div className="mt-16 bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-3xl font-bold mb-6 text-center">
            Why GEO Gap Compass?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="font-semibold text-lg mb-2">🎯 Find Citation Gaps</h3>
              <p className="text-gray-600">
                Identify topics where your brand should appear but doesn't
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-2">📊 Track Competitors</h3>
              <p className="text-gray-600">
                See how your visibility compares to competitors
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-2">🚀 Get Actionable Insights</h3>
              <p className="text-gray-600">
                AI-powered recommendations to improve your GEO strategy
              </p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-12 text-center">
          <p className="text-gray-700 mb-4">
            Ready to optimize your AI visibility?
          </p>
          <button
            onClick={() => router.push("/dashboard")}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-lg transition"
          >
            Start Analyzing Now
          </button>
        </div>
      </div>
    </div>
  );
}
