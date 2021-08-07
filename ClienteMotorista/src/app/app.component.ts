import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  title = 'ClienteMotorista';
  serverData: any
  employeeData: any;
  employee:any;
  IdUser: any; 
  idCorrida: any; 
  listadeViagens:any;

  constructor(private httpClient: HttpClient) {
  }

  ngOnInit() {
  }

  sayHi() {
    this.httpClient.get('http://127.0.0.1:5002/').subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
    })
  }

  Cadastro(nome:any, telefone:any) {
    this.httpClient.post('http://127.0.0.1:5002/servidor/cadastro/' + nome + '/'+ telefone + '/1', "").subscribe(data => {
      this.IdUser = data as JSON;
      console.log(this.IdUser);
    })
  }

  ConsultaViagens(origem:any, destino:any, data:any) {
    
    this.httpClient.get('http://127.0.0.1:5002/servidor/consulta/' + origem + '/'+ destino + '/'+ data + '/1').subscribe(data => {
      this.listadeViagens = data as JSON;
      console.log(this.listadeViagens);
    })
    this.InteresseEmPassageiro(origem, destino, data)
  }

  InteresseEmPassageiro(origem:any, destino:any, data:any) {
    if(this.IdUser){
      this.httpClient.post('http://127.0.0.1:5002/servidor/interesseEmPassageiro/' + this.IdUser + '/' + origem + '/'+ destino + '/'+ data , "").subscribe(data => {
        this.idCorrida = data as JSON;
        console.log(this.idCorrida);
      })
    }else{
      console.log("SEM USUARIO")
    }
  }

  removeInteresseEmPassageiro(idCorrida:any) {
    this.httpClient.delete('http://127.0.0.1:5002/servidor/removeInteresseEmPassageiro/' + idCorrida).subscribe(data => {
      this.listadeViagens = data as JSON;
      console.log(this.listadeViagens)
    })
  }
}
