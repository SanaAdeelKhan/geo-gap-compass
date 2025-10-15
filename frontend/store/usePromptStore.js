// FILE: store/usePromptStore.js
import { create } from "zustand";
import { persist } from "zustand/middleware";

const usePromptStore = create(
  persist(
    (set) => ({
      results: null,
      setResults: (data) => set({ results: data }),
      clearResults: () => set({ results: null }),
    }),
    {
      name: "prompt-results-storage", // key in localStorage
    }
  )
);

export default usePromptStore;
