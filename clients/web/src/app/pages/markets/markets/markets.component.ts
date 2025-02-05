import { Component } from '@angular/core';
import { CardModule } from 'primeng/card';

@Component({
  selector: 'app-markets',
  standalone: true,
  imports: [CardModule],
  templateUrl: './markets.component.html',
  styleUrl: './markets.component.css',
})
export class MarketsComponent {}
