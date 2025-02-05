import { Routes } from '@angular/router';
import { IndexComponent } from './pages/index/index.component';
import { MarketsComponent } from './pages/markets/markets/markets.component';
import { MarketComponent } from './pages/markets/market/market.component';

export const routes: Routes = [
  {
    title: 'Simplgrocr',
    path: '',
    component: IndexComponent,
  },
  {
    title: 'Simplgrocr',
    path: 'markets',
    component: MarketsComponent,
  },
  {
    title: 'Simplgrocr',
    path: 'markets/:id',
    component: MarketComponent,
  },
];
