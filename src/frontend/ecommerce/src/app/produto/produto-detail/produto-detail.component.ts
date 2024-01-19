import { Component, Input, OnInit } from '@angular/core';
import { Produto } from  '../models/produto'

@Component({
  selector: 'produto-detail',
  templateUrl: './produto-detail.component.html',
  styleUrls: ['./produto-detail.component.css']
})
export class ProdutoDetailComponent implements OnInit {

  @Input()
  produto!: Produto;

  constructor() { }

  ngOnInit() {
    
  }

}
