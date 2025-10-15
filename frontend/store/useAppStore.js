// FILE: store/useAppStore.js
import { create } from "zustand";
import { persist } from "zustand/middleware";

// ✅ Global store with automatic localStorage persistence
export const useAppStore = create(
  persist(
    (set) => ({
      // ====== Global States ======
      promptResults: null,
      gapHeatmapData: null,
      competitorData: null,
      insightsData: null,

      // ====== Actions ======
      setPromptResults: (data) => set({ promptResults: data }),
      clearPromptResults: () => set({ promptResults: null }),

      setGapHeatmapData: (data) => set({ gapHeatmapData: data }),
      clearGapHeatmapData: () => set({ gapHeatmapData: null }),

      setCompetitorData: (data) => set({ competitorData: data }),
      clearCompetitorData: () => set({ competitorData: null }),

      setInsightsData: (data) => set({ insightsData: data }),
      clearInsightsData: () => set({ insightsData: null }),
    }),
    {
      name: "geo-gap-store", // key in localStorage
    }
  )
);
