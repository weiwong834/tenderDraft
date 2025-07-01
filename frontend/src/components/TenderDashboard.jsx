import React, { useState } from "react";
import { Search, FileText, DollarSign, CheckCircle } from "lucide-react";

const TenderDashboard = () => {
  const [tenderId, setTenderId] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeTender = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/analyze-tender", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          tender_id: tenderId,
          tender_url: null,
        }),
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();

      // Transform API response to match your current format
      setAnalysis({
        title: data.title,
        priceRange: {
          min: data.price_range.min,
          max: data.price_range.max,
        },
        confidence: data.confidence,
        requirements: data.requirements,
        compliance: data.compliance,
      });
    } catch (error) {
      console.error("Error analyzing tender:", error);
      alert("Failed to analyze tender. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Toptimize</h1>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex gap-4 mb-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Enter Tender ID or URL"
                value={tenderId}
                onChange={(e) => setTenderId(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={analyzeTender}
              disabled={loading || !tenderId}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
            >
              <Search size={20} />
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </div>
        </div>

        {analysis && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <DollarSign className="text-green-600" />
                Optimal Bid Range
              </h2>
              <div className="text-3xl font-bold text-green-600 mb-2">
                €{analysis.priceRange.min.toLocaleString()} - €
                {analysis.priceRange.max.toLocaleString()}
              </div>
              <div className="text-sm text-gray-600">
                Confidence: {analysis.confidence}%
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <CheckCircle className="text-blue-600" />
                Compliance Score
              </h2>
              <div className="text-3xl font-bold text-blue-600 mb-2">
                {analysis.compliance}%
              </div>
              <div className="text-sm text-gray-600">
                Based on requirements analysis
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6 md:col-span-2">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <FileText className="text-purple-600" />
                Key Requirements
              </h2>
              <ul className="space-y-2">
                {analysis.requirements.map((req, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <CheckCircle size={16} className="text-green-500 mt-1" />
                    <span>{req}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TenderDashboard;
