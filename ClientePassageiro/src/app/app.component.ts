import { HttpClient } from '@angular/common/http';
import {Component, Inject} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  title = 'ClientePassageiro';
  serverData: any
  nome: any;
  telefone:any;
  IdUser: any; 
  idCorrida: any; 
  listadeViagens:any;
  eventSource:any;
  page:any = 1;
  aviso:any;
  constructor(private httpClient: HttpClient, public dialog: MatDialog) {
  }
  openDialog(): void {
    const dialogRef = this.dialog.open(AppComponent, {
      width: '250px',
      data: {name: this.aviso}
    });
  }
  ngOnInit() {
   }
  Cadastro(nome:any, telefone:any) {
    this.nome = nome;
    this.telefone = telefone;
    this.page = 2;
    this.httpClient.post('http://127.0.0.1:5002/servidor/cadastro/' + nome + '/'+ telefone + '/0', "").subscribe(data => {
      this.IdUser = data as JSON;
      console.log(this.IdUser);
    })
  }

  ConsultaViagens(origem:any, destino:any, data:any, qtdePassageiros:any, interesse: any) {
    data = String(data).replace("/", "" )
    data = String(data).replace("/", "" )
    this.httpClient.get('http://127.0.0.1:5002/servidor/consulta/' + origem + '/'+ destino + '/'+ data + '/0').subscribe(data => {
      this.listadeViagens = data as JSON;
      console.log(this.listadeViagens);
    })
    if(interesse){
      this.InteresseEmCarona(origem, destino, data, qtdePassageiros)
    }
  }

  InteresseEmCarona(origem:any, destino:any, data:any, qtdePassageiros:any) {
    if(this.IdUser){
      this.httpClient.post('http://127.0.0.1:5002/servidor/interesseEmCarona/' + this.IdUser + '/' + origem + '/'+ destino + '/'+ data + '/'+ qtdePassageiros, "").subscribe(response => {
        this.idCorrida = response  as JSON;
        console.log(this.idCorrida);
        // this.NotificaMotorista(origem, destino, data)
      })
    }else{
      console.log("SEM USUARIO")
    }
  }

  // NotificaMotorista(origem:any, destino:any, data:any){
  
  //   this.eventSource = new EventSource("http://127.0.0.1:5002/listen/" + origem + '/'+ destino + '/'+ data)

  //   this.aviso = this.eventSource.addEventListener("message",  function(e:any) {
  //     console.log(e.data)
  //   },  false)
  //   this.aviso = this.eventSource.addEventListener("online", function(e:any) {
  //     console.log(e)
  //   },true)
  // }

  removeInteresseEmPassageiro(idCorrida:any) {
    this.httpClient.delete('http://127.0.0.1:5002/servidor/removeInteresseEmCarona/' + idCorrida).subscribe(data => {
      this.listadeViagens = data as JSON;
      console.log(this.listadeViagens)
    })
  }
}
