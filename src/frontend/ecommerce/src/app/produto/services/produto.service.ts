import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Produto } from '../models/produto';

const GET_PRODUTOS_API = 'http://127.0.0.1:8000/produtos/'


@Injectable({
    providedIn: 'root',
})


export class ProdutoService {

constructor(private http: HttpClient) {

}

getProdutos() : Observable<any>{
    return this.http.get<any>(GET_PRODUTOS_API + '?latitudeCliente=-15&longitudeCliente=-45')
}

}
