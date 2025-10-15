"use client";
import { useState, useEffect } from "react";
import { healthCheck } from "@/utils/api";
import Link from "next/link";
import { 
  TrendingUp, 
  Users, 
  Globe, 
  BarChart3,
  AlertCircle 
} from "lucide-react";

export default function DashboardPage() {
  const [apiStatus, setApiStatus] = useState(null);

  useEffect(() => {
    const checkAPI = async () => {
      try {
        const status = await healthCheck();
        setApiStatus(status);
      } catch (err) {
        setApiStatus({ status: "error", openai_enabled: false });
      }
    };
    checkAPI();
  }, []);

  const dashboardCards = [
    {
      title: "Prompt Testing",
      description: "Test brand visibility across AI prompts",
      icon: BarChart3,
      href: "/dashboard/prompts",
      color: "blue"
    },
    {
      title: "Gap Heatmap",
      description: "Visualize citation gaps by content type",
      icon: TrendingUp,
      href: "/dashboard/heatmap",
      color: "red"
    },
    {
      title: "Competitor Analysis",
      description: "Compare your brand with competitors",
      icon: Users,
      href: "/dashboard/competitors",
      color: "green"
    },
    {
      title: "Domain Insights",
      description: "Analyze domain authority and relevance",
      icon: Globe,
      href: "/dashboard/domains",
      color: "purple"
    }
  ];

  const colorClasses = {
    blue: "bg-blue-50 border-blue-200 hover:bg-blue-100",
    red: "bg-red-50 border-red-200 hover:bg-red-100",
    green: "bg-green-50 border-green-200 hover:bg-green-100",
    purple: "bg-purple-50 border-purple-200 hover:bg-purple-100"
  };

  const iconColorClasses = {
    blue: "text-blue-600",
    red: "text-red-600",
    green: "text-green-600",
    purple: "text-purple-600"
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-gray-900">
            GEO Gap Compass Dashboard
          </h1>
          <p className="text-gray-600 mt-1">
            AI-Powered Brand Visibility Analytics
          </p>
        </div>
      </div>

      {/* API Status Banner */}
      <div className="max-w-7xl mx-auto px-6 py-4">
        {apiStatus && (
          <div className={`p-4 rounded-lg border ${
            apiStatus.openai_enabled 
              ? "bg-green-50 border-green-200" 
              : "bg-yellow-50 border-yellow-200"
          }`}>
            <div className="flex items-center gap-3">
              <AlertCircle className={
                apiStatus.openai_enabled ? "text-green-600" : "text-yellow-600"
              } size={20} />
              <div>
                <p className="font-medium">
                  {apiStatus.openai_enabled 
                    ? "✅ OpenAI Connected - Using Real AI Analysis" 
                    : "⚠️ OpenAI Unavailable - Using Mock Data"}
                </p>
                <p className="text-sm text-gray-600">
                  API Status: {apiStatus.status}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Dashboard Cards */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {dashboardCards.map((card) => (
            <Link key={card.title} href={card.href}>
              <div className={`p-6 rounded-lg border-2 transition cursor-pointer ${
                colorClasses[card.color]
              }`}>
                <card.icon className={`mb-4 ${iconColorClasses[card.color]}`} size={32} />
                <h3 className="font-semibold text-lg mb-2">{card.title}</h3>
                <p className="text-sm text-gray-600">{card.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <h2 className="text-xl font-semibold mb-4">Quick Stats</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <p className="text-gray-600 text-sm">Total Prompts Tested</p>
            <p className="text-3xl font-bold text-blue-600 mt-2">0</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <p className="text-gray-600 text-sm">Citation Gaps Found</p>
            <p className="text-3xl font-bold text-red-600 mt-2">0</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <p className="text-gray-600 text-sm">Competitors Analyzed</p>
            <p className="text-3xl font-bold text-green-600 mt-2">0</p>
          </div>
        </div>
      </div>
    </div>
  );
}