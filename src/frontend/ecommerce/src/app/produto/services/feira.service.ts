import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

const GET_FEIRAS_API = 'http://localhost:8000/feira/';

@Injectable({
    providedIn: 'root',
})
export class FeiraService {

constructor(private http: HttpClient) { }

getFeiras():any{
    return this.http.get<any>(GET_FEIRAS_API)
}

}
