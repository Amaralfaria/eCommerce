/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { BancaService } from './banca.service';

describe('Service: Banca', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [BancaService]
    });
  });

  it('should ...', inject([BancaService], (service: BancaService) => {
    expect(service).toBeTruthy();
  }));
});
