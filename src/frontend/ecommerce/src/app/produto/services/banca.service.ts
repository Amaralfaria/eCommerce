import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

const GET_BANCAS_API = 'http://localhost:8000/fornecedores/';

@Injectable({
    providedIn: 'root',
})
export class BancaService {

constructor(private http: HttpClient) { }

getBancas(): any{
   return this.http.get<any>(GET_BANCAS_API)
}

}
