import { Component, OnInit } from '@angular/core';
import { Filtro } from './filtros';
import { Feira } from '../models/produto';
import { FeiraService } from '../services/feira.service';

@Component({
  selector: 'filtro',
  templateUrl: './filtro.component.html',
  styleUrls: ['./filtro.component.css']
})

export class FiltroComponent implements OnInit {

  constructor(private feiraService: FeiraService) { 
  }

  filtros!: Filtro;
  feiras!: Feira[];

  ngOnInit() {
    this.feiraService.getFeiras().subscribe((data:any)=>{
      this.feiras = data.feiras;
    })
  }

  handleSubmit(filtroForm: any){
    
  }

}
