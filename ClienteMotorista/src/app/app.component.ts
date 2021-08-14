import { HttpClient } from '@angular/common/http';
import {Component, Inject} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  title = 'ClienteMotorista';
  serverData: any
  nome: any;
  telefone:any;
  IdUser: any; 
  viagensDoUsuario:any = 0;
  idCorrida: any; 
  listadeViagens:any = 0;
  eventSource:any;
  page:any = 1;
  aviso:any;
  URL: any;
  countUser:any;
  constructor(private httpClient: HttpClient, public dialog: MatDialog) {
  }
  openDialog(): void {
    const dialogRef = this.dialog.open(AppComponent, {
      width: '250px',
      data: {name: this.aviso}
    });
  }
  ngOnInit() {
    this.httpClient.get('http://127.0.0.1:5002/servidor/TamanhoLista/'+ '1').subscribe(data => {
      this.countUser = data as JSON;
      console.log(this.countUser);
      this.eventSource = new EventSource("http://127.0.0.1:5002/stream?channel=" + String(this.countUser))
      this.eventSource.addEventListener('publish',  function(e:any) {
          console.log(e.data)
      },  true)
    })
    
   }
  Cadastro(nome:any, telefone:any) {

    this.nome = nome;
    this.telefone = telefone;
    this.page = 2;
    this.httpClient.post('http://127.0.0.1:5002/servidor/cadastro/' + nome + '/'+ telefone + '/1', "").subscribe(data => {
      this.IdUser = data as JSON;
      console.log(this.IdUser);
      
    })
  }

  MinhasViagens() {
    this.page = 3;
    this.httpClient.get('http://127.0.0.1:5002/servidor/consultaViagensDoUsuario/' + this.IdUser  + '/1').subscribe(data => {
      this.viagensDoUsuario = data as JSON;
      console.log(this.viagensDoUsuario);
      
    })
  }

  ConsultaViagens(origem:any, destino:any, data:any) {
    data = String(data).replace("/", "" )
    data = String(data).replace("/", "" )
    this.httpClient.get('http://127.0.0.1:5002/servidor/consulta/' + origem + '/'+ destino + '/'+ data + '/1').subscribe(data => {
      this.listadeViagens = data as JSON;
      console.log(this.listadeViagens);
    })
  }

  InteresseEmPassageiro(origem:any, destino:any, data:any) {
    data = String(data).replace("/", "" )
    data = String(data).replace("/", "" )
    if(this.IdUser){
      this.httpClient.post('http://127.0.0.1:5002/servidor/interesseEmPassageiro/' + this.IdUser + '/' + origem + '/'+ destino + '/'+ data , "").subscribe(response => {
        this.idCorrida = response  as JSON;
        console.log(this.idCorrida);
        this.NotificaMotorista(origem, destino, data)
      })
    }else{
      console.log("SEM USUARIO")
    }
  }

  NotificaMotorista(origem:any, destino:any, data:any){
  
    // this.eventSource = new EventSource("http://127.0.0.1:5002/listen/" + origem + '/'+ destino + '/'+ data)

    // this.eventSource.addEventListener("message",  function(e:any) {
    //   console.log(e.data)
    // },  false)
  }

  removeInteresseEmPassageiro(idCorrida:any) {
    this.httpClient.delete('http://127.0.0.1:5002/servidor/removeInteresseEmPassageiro/' + idCorrida).subscribe(data => {
      this.listadeViagens = data as JSON;
      console.log(this.listadeViagens)
    })
  }
}
