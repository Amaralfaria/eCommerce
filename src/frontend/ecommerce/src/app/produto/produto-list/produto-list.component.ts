import { Component, OnInit } from '@angular/core';
import { ProdutoService } from '../services/produto.service';
import { Produto } from '../models/produto';

@Component({
  selector: 'produto-list',
  templateUrl: './produto-list.component.html',
  styleUrls: ['./produto-list.component.css']
})
export class ProdutoListComponent implements OnInit {
  
  constructor(private produtoService: ProdutoService) { }
  
  produtos!: Produto[]

  ngOnInit() {
    this.produtoService.getProdutos().subscribe((data : any) => {
      this.produtos = data.produtos;
    })
  }

}
