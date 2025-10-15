// utils/api.js - Fixed API functions
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Get domain insights with OpenAI analysis
 * Priority: DuckDuckGo → OpenAI → Mock Data
 */
export async function getDomainInsights(brand, domains, analysisType = "comprehensive") {
  if (!brand || !domains || domains.length === 0) {
    throw new Error("Brand and domains are required");
  }

  // Ensure domains is an array
  const domainArray = Array.isArray(domains) 
    ? domains 
    : domains.split(",").map(d => d.trim());

  const response = await fetch(`${BASE_URL}/insights/analyze-domains`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      brand,
      domains: domainArray,
      analysis_type: analysisType,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API ${response.status}: ${errorText}`);
  }

  return await response.json();
}

/**
 * Get domain statistics with optional AI analysis
 */
export async function getDomainStats(brand, domainsString, includeAI = true) {
  const domains = domainsString
    .split(",")
    .map(d => d.trim())
    .join(",");

  const params = new URLSearchParams({
    domains,
    brand,
    include_ai_analysis: includeAI,
  });

  const response = await fetch(
    `${BASE_URL}/insights/domain-stats?${params.toString()}`,
    { headers: { "Content-Type": "application/json" } }
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch domain stats: ${response.statusText}`);
  }

  return await response.json();
}

/**
 * Compare your domains with competitor domains
 */
export async function compareDomains(brand, yourDomains, competitorDomains) {
  const params = new URLSearchParams({
    brand,
    your_domains: yourDomains.join(","),
    competitor_domains: competitorDomains.join(","),
  });

  const response = await fetch(
    `${BASE_URL}/insights/domain-comparison?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to compare domains");
  }

  return await response.json();
}

/**
 * Get trending topics for a brand
 */
export async function getTrendingTopics(brand, domains = [], numTopics = 5) {
  const params = new URLSearchParams({
    brand,
    num_topics: numTopics,
  });

  if (domains.length > 0) {
    params.append("domains", domains.join(","));
  }

  const response = await fetch(
    `${BASE_URL}/insights/trending-topics?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch trending topics");
  }

  return await response.json();
}

/**
 * Test prompts - core functionality
 */
export async function testPrompts(brand, promptVariations = null) {
  const body = {
    brand,
    ...(promptVariations && { prompt_variations: promptVariations }),
  };

  const response = await fetch(`${BASE_URL}/prompts/test`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error("Failed to test prompts");
  }

  return await response.json();
}

/**
 * Generate a single prompt response with citations
 */
export async function generateSinglePrompt(brand, prompt) {
  const response = await fetch(`${BASE_URL}/prompts/single`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ brand, prompt }),
  });

  if (!response.ok) {
    throw new Error("Failed to generate prompt response");
  }

  return await response.json();
}

/**
 * Get available prompt templates
 */
export async function getPromptTemplates() {
  const response = await fetch(`${BASE_URL}/prompts/templates`);

  if (!response.ok) {
    throw new Error("Failed to fetch prompt templates");
  }

  return await response.json();
}

/**
 * Generate prompt variations using AI
 */
export async function generatePromptVariations(
  brand,
  basePrompt,
  numVariations = 5
) {
  const params = new URLSearchParams({
    brand,
    base_prompt: basePrompt,
    num_variations: numVariations,
  });

  const response = await fetch(
    `${BASE_URL}/prompts/generate-variations?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to generate variations");
  }

  return await response.json();
}

/**
 * Analyze competitors
 */
export async function analyzeCompetitors(brand, competitors) {
  const response = await fetch(`${BASE_URL}/analyze_competitors/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      brand,
      competitors: Array.isArray(competitors) 
        ? competitors 
        : competitors.split(",").map(c => c.trim()),
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to analyze competitors");
  }

  return await response.json();
}

/**
 * Get content gap heatmap (legacy endpoint)
 * Note: there are two possible backend routes for heatmaps in earlier discussion:
 * - /gap_heatmap/ (if implemented)
 * - /citations/brand-gap (preferred)
 *
 * Keep this generic function for backward compatibility if you implemented /gap_heatmap.
 */
export async function getGapHeatmap(brand, missingTopics) {
  const params = new URLSearchParams({
    brand,
    missing_topics: Array.isArray(missingTopics)
      ? missingTopics.join(",")
      : missingTopics,
  });

  const response = await fetch(`${BASE_URL}/gap_heatmap/?${params.toString()}`);

  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(`Failed to fetch gap heatmap: ${response.status} ${text}`);
  }

  return await response.json();
}

/**
 * Extract URLs from text
 */
export async function extractUrls(text) {
  const params = new URLSearchParams({ text });

  const response = await fetch(`${BASE_URL}/citations/extract?${params.toString()}`);

  if (!response.ok) {
    throw new Error("Failed to extract URLs");
  }

  return await response.json();
}

/**
 * Analyze brand presence by prompt type
 */
export async function analyzeBrandPresence(brand, promptTypes) {
  const params = new URLSearchParams({
    brand,
    prompt_types: Array.isArray(promptTypes)
      ? promptTypes.join(",")
      : promptTypes,
  });

  const response = await fetch(
    `${BASE_URL}/citations/brand-missing?${params.toString()}`
  );

  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(`Failed to analyze brand presence: ${response.status} ${text}`);
  }

  return await response.json();
}

/**
 * Health check - verify API and OpenAI availability
 */
export async function healthCheck() {
  try {
    const response = await fetch(`${BASE_URL}/health`);
    if (!response.ok) throw new Error("Health check failed");
    return await response.json();
  } catch (err) {
    return {
      status: "error",
      openai_enabled: false,
      error: err.message,
    };
  }
}

/* ============================================================
   Heatmap helpers (NEW)
   - getBrandGapHeatmap: calls backend /citations/brand-gap and returns numeric rows
   - buildHeatmapFromBrandMissing: calls /citations/brand-missing and converts to numeric rows
   ============================================================ */

/**
 * Call backend /citations/brand-gap which should return structured numeric heatmap:
 * { brand, competitor, data: [{ promptType, yourBrandScore, competitorScore }, ...], using_openai, is_mock }
 */
export async function getBrandGapHeatmap(brand, competitor) {
  if (!brand) throw new Error("brand is required");
  const params = new URLSearchParams({
    brand,
    competitor: competitor || "",
  });

  const res = await fetch(`${BASE_URL}/citations/brand-gap?${params.toString()}`);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to fetch brand-gap: ${res.status} ${text}`);
  }
  const payload = await res.json();
  // Ensure payload.data shape is normalized
  if (payload && Array.isArray(payload.data)) {
    return payload;
  }
  // If backend returned structured_analysis or another shape, just return raw payload
  return payload;
}

/**
 * Heuristic: convert /citations/brand-missing response into numeric heatmap rows.
 *
 * Input (brand-missing) shape:
 * {
 *   brand,
 *   prompt_types_analyzed: ["how-to","comparison",...],
 *   missing_prompt_types: [...],
 *   strong_prompt_types: [...]
 *   ...
 * }
 *
 * Output:
 * {
 *   brand,
 *   competitor: null,
 *   data: [{ promptType, yourBrandScore, competitorScore }, ...],
 *   using_openai,
 *   is_mock,
 *   raw: payload
 * }
 *
 * Scoring heuristic (tweakable):
 * - if prompt in missing -> your=25 competitor=75
 * - if prompt in strong  -> your=85 competitor=45
 * - neutral/default      -> your=55 competitor=65
 */
export async function buildHeatmapFromBrandMissing(brand, promptTypes = null) {
  if (!brand) throw new Error("brand is required");

  const params = new URLSearchParams({
    brand,
    prompt_types: promptTypes ? (Array.isArray(promptTypes) ? promptTypes.join(",") : promptTypes) : "",
  });

  const res = await fetch(`${BASE_URL}/citations/brand-missing?${params.toString()}`);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to fetch brand-missing: ${res.status} ${text}`);
  }

  const payload = await res.json();

  const prompts = payload.prompt_types_analyzed || [];
  const missingSet = new Set((payload.missing_prompt_types || []).map(p => p.toLowerCase()));
  const strongSet = new Set((payload.strong_prompt_types || []).map(p => p.toLowerCase()));

  const rows = prompts.map(pt => {
    const key = (pt || "").toLowerCase();
    if (missingSet.has(key)) {
      return { promptType: pt, yourBrandScore: 25, competitorScore: 75 };
    }
    if (strongSet.has(key)) {
      return { promptType: pt, yourBrandScore: 85, competitorScore: 45 };
    }
    // default neutral
    return { promptType: pt, yourBrandScore: 55, competitorScore: 65 };
  });

  return {
    brand: payload.brand || brand,
    competitor: null,
    data: rows,
    using_openai: payload.using_openai || false,
    is_mock: payload.is_mock || false,
    raw: payload,
  };
}
