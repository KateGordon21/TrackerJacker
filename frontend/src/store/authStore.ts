import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import axios from "axios";

// Define types for the store's state
interface User {
  id: number;
  username: string;
}

interface AuthState {
  user: User | null; // user data
  token: string | null; // authentication token
  loading: boolean; // loading state for async actions
  authError: string | null; // error message for failed actions
  isAuthenticated: boolean;

  setAuthData: (user: User, token: string) => void; // Set user and token
  clearAuthData: () => void; // Clear user and token
  setLoading: (loading: boolean) => void; // Set loading state
  setError: (authError: string | null) => void; // Set error state
  setIsAuthenticated: (isAuthenticated: boolean) => void;

  register: (userData: {
    username: string;
    password: string;
    password2: string;
  }) => void; // Register user
  login: (credentials: { username: string; password: string }) => void; // Login user
  logout: () => void; // Logout user
  deleteUser: () => void; // Delete the current user
  fetchUserDetails: () => void; // Fetch user details
  getUserById: (id: number) => void; // Get user details by ID
  getUserByUsername: (username: string) => void; // Get user details by username
  updateUser: (updatedData: Partial<User>) => void; // Update user details
}

// Create axios instance with baseURL from environment variable
const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || "",
});

// Create the auth store with Zustand and persist middleware
const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      loading: false,
      authError: null,
      isAuthenticated: false,

      // Set user and token
      setAuthData: (user, token) => {
        set({ user, token, authError: null, isAuthenticated: true });
      },

      // Clear user and token
      clearAuthData: () => {
        set({ user: null, token: null, isAuthenticated: false });
      },

      // Set loading state
      setLoading: (loading) => {
        set({ loading });
      },

      // Set error state
      setError: (authError) => {
        set({ authError });
      },

      setIsAuthenticated: (isAuthenticated) => {
        set({ isAuthenticated });
      },

      // Register user (axios call)
      register: async (userData) => {
        try {
          set({ loading: true });
          const response = await api.post("/api/auth/register/", userData);

          set({
            authError: null,
            user: response.data.user,
            token: response.data.token,
            loading: false,
            isAuthenticated: true,
          });
        } catch (error: any) {
          set({
            authError:
              error.response?.data?.detail?.password ||
              error.response?.data?.detail?.username ||
              error.response?.data?.detail ||
              "An error occurred while registering.",
            loading: false,
          });
        }
      },

      // Login user (axios call)
      login: async (credentials) => {
        try {
          set({ loading: true });
          const response = await api.post("/api/auth/login/", credentials);

          set({
            user: response.data.user,
            token: response.data.token,
            loading: false,
            isAuthenticated: true,
          });
        } catch (error: any) {
          set({
            authError:
              error.response?.data?.detail?.password ||
              error.response?.data?.detail?.username ||
              error.response?.data?.detail ||
              "An error occurred while logging in.",
            loading: false,
          });
        }
      },

      // Logout user
      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
      },

      // Delete the currently authenticated user (axios call)
      deleteUser: async () => {
        try {
          set({ loading: true });
          const response = await api.delete("/api/auth/delete/", {
            headers: {
              Authorization: `Token ${get().token}`,
            },
          });

          set({
            user: null,
            token: null,
            loading: false,
            isAuthenticated: false,
          });
        } catch (error: any) {
          set({
            authError:
              error.response?.data?.detail ||
              "An error occurred while deleting the user.",
            loading: false,
          });
        }
      },

      // Fetch user details (axios call)
      fetchUserDetails: async () => {
        try {
          set({ loading: true });
          const response = await api.get("/api/auth/user/", {
            headers: {
              Authorization: `Token ${get().token}`,
            },
          });

          set({ user: response.data, loading: false });
        } catch (error: any) {
          set({
            authError:
              error.response?.data?.detail ||
              "An error occurred while fetching user details.",
            loading: false,
          });
        }
      },

      // Get user details by ID (axios call)
      getUserById: async (id) => {
        try {
          set({ loading: true });
          const response = await api.get(`/api/auth/get/${id}/`, {
            headers: {
              Authorization: `Token ${get().token}`,
            },
          });

          set({ user: response.data, loading: false });
        } catch (error: any) {
          set({
            authError:
              error.response?.data?.detail ||
              "An error occurred while fetching user by ID.",
            loading: false,
          });
        }
      },

      // Get user details by username (axios call)
      getUserByUsername: async (username) => {
        try {
          set({ loading: true });
          const response = await api.get(`/api/auth/get/${username}/`, {
            headers: {
              Authorization: `Token ${get().token}`,
            },
          });

          set({ user: response.data, loading: false });
        } catch (error: any) {
          set({
            authError:
              error.response?.data?.detail ||
              "An error occurred while fetching user by username.",
            loading: false,
          });
        }
      },

      // Update user details (axios call)
      updateUser: async (updatedData) => {
        try {
          set({ loading: true });
          const response = await api.put("/api/auth/update/", updatedData, {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Token ${get().token}`,
            },
          });

          set({ user: response.data, loading: false });
        } catch (error: any) {
          set({
            authError:
              error.response?.data?.detail ||
              "An error occurred while updating user details.",
            loading: false,
          });
        }
      },
    }),
    {
      name: "auth-storage", // You can give your localStorage key a custom name
      storage: createJSONStorage(() => localStorage), // Persist using localStorage
    }
  )
);

export default useAuthStore;
