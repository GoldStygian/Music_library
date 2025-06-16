import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter, withDebugTracing } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { routes } from './app.routes';


export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withDebugTracing()),
    provideHttpClient(
      withFetch() //use the Fetch API instead of XMLHttpRequests
    ),
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true })
  ]
};
