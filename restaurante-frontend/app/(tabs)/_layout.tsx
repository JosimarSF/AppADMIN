import { Tabs } from 'expo-router';
import React from 'react';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

const COLORS = {
  primary: '#FA7F08',
  background: '#FFFFFF',
  gray: '#E0E0E0',
  inactive: '#A0A0A0',
};

export default function TabLayout() {
  const { bottom } = useSafeAreaInsets();

  const tabBarIcon = (focused: boolean, active: string, inactive: string, color: string) => (
    <Ionicons name={focused ? active : inactive} size={26} color={color} />
  );

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        unmountOnBlur: false,
        lazy: false,
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.inactive,
        tabBarStyle: {
          backgroundColor: COLORS.background,
          borderTopWidth: 0.5,
          borderTopColor: COLORS.gray,
          height: 60 + bottom,
          paddingBottom: bottom > 0 ? bottom - 5 : 10,
          paddingTop: 8,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
          marginTop: -2,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Menú',
          tabBarIcon: ({ color, focused }) =>
            tabBarIcon(focused, 'restaurant', 'restaurant-outline', color),
        }}
      />

      <Tabs.Screen
        name="cart"
        options={{
          title: 'Carrito',
          tabBarIcon: ({ color, focused }) =>
            tabBarIcon(focused, 'cart', 'cart-outline', color),
        }}
      />

      <Tabs.Screen
        name="orders/index"
        options={{
          title: 'Pedidos',
          tabBarIcon: ({ color, focused }) =>
            tabBarIcon(focused, 'receipt', 'receipt-outline', color),
        }}
      />
    </Tabs>
  );
}
