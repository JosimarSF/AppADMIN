import { ThemeProvider, DarkTheme, DefaultTheme } from '@react-navigation/native';
import { Stack, useRouter } from 'expo-router';
import 'react-native-reanimated';
import { useColorScheme } from '@/hooks/use-color-scheme';
import AuthProvider, { useAuth } from '../context/AuthContext';
import { CartProvider } from '../context/CartContext';
import { OrderProvider } from '../context/OrderContext';
import { useEffect } from 'react';

function NavigationController() {
  const { token, user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return;

    // No autenticado → login
    if (!token) {
      router.replace('/(auth)/login');
      return;
    }

    // Admin → carpeta (admin)
    if (user?.role === 'admin') {
      router.replace('/(admin)');
      return;
    }

    // Cliente → tabs
    router.replace('/(tabs)');
  }, [token, user, isLoading]);

  return null; 
}

export default function RootLayout() {
  const colorScheme = useColorScheme();

  return (
    <AuthProvider>
      <CartProvider>
        <OrderProvider>
          <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>

            <NavigationController />

            <Stack screenOptions={{ headerShown: false }}>
              <Stack.Screen name="(tabs)" />
              <Stack.Screen name="(auth)" />
              <Stack.Screen name="(admin)" /> 
              <Stack.Screen name="orders/[id]" />
            </Stack>

          </ThemeProvider>
        </OrderProvider>
      </CartProvider>
    </AuthProvider>
  );
}
