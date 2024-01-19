/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { FeiraService } from './feira.service';

describe('Service: Feira', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [FeiraService]
    });
  });

  it('should ...', inject([FeiraService], (service: FeiraService) => {
    expect(service).toBeTruthy();
  }));
});
