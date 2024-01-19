import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProdutoComponent } from './produto.component';
import { HttpClientModule } from '@angular/common/http';
import { ProdutoListComponent } from './produto-list/produto-list.component';
import { ProdutoDetailComponent } from './produto-detail/produto-detail.component';
import { ProdutoService } from './services/produto.service';
import { FormsModule } from '@angular/forms';
import { FiltroComponent } from './filtro/filtro.component';
import { FeiraService } from './services/feira.service';

@NgModule({
  declarations: [ProdutoComponent, ProdutoListComponent, ProdutoDetailComponent, FiltroComponent],
  imports: [
    CommonModule, HttpClientModule, FormsModule,
  ],
  providers: [ProdutoService,FeiraService],
  exports: [ProdutoComponent,ProdutoListComponent,FiltroComponent],
})
export class ProdutoModule { }
