import { Tabs, Redirect } from "expo-router";
import React from "react";
import { Ionicons } from "@expo/vector-icons";
import { useAuth } from "@/context/AuthContext";

const COLORS = {
  primary: "#FA7F08",
  background: "#FFFFFF",
  gray: "#E0E0E0",
  inactive: "#A0A0A0",
};

export default function AdminTabLayout() {
  const { user, isLoading } = useAuth();

  if (isLoading) return null;

  if (!user) return <Redirect href="/(auth)/login" />;
  if (user.role !== "admin") return <Redirect href="/(tabs)" />;

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.inactive,
        tabBarStyle: {
          backgroundColor: COLORS.background,
          borderTopWidth: 0.5,
          borderTopColor: COLORS.gray,
        },
      }}
    >
      <Tabs.Screen
        name="dashboard"
        options={{
          title: "Dashboard",
          tabBarIcon: ({ color, focused }) => (
            <Ionicons
              name={focused ? "grid" : "grid-outline"}
              size={26}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="products"
        options={{
          title: "Productos",
          tabBarIcon: ({ color, focused }) => (
            <Ionicons
              name={focused ? "fast-food" : "fast-food-outline"}
              size={26}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="orders"
        options={{
          title: "Pedidos",
          tabBarIcon: ({ color, focused }) => (
            <Ionicons
              name={focused ? "receipt" : "receipt-outline"}
              size={26}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="users"
        options={{
          title: "Usuarios",
          tabBarIcon: ({ color, focused }) => (
            <Ionicons
              name={focused ? "people" : "people-outline"}
              size={26}
              color={color}
            />
          ),
        }}
      />
    </Tabs>
  );
}
