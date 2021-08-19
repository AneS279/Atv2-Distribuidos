import { HttpClient } from '@angular/common/http';
import {Component, Inject} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {MatSnackBar} from '@angular/material/snack-bar';

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
  viagensDoUsuario:any = 0;
  idCorrida: any; 
  listadeViagens:any = 0;
  eventSource:any;
  interesseRegistrado:any = 0;
  page:any = 1;
  aviso:any;
  URL: any;
  countUser:any;
  motoristaInfo:any = [];
  constructor(private httpClient: HttpClient, public dialog: MatDialog, private _snackBar: MatSnackBar) {
  }
  openSnackBar(message:any, action:any) {
    this._snackBar.open(message,action);
  }
  ngOnInit() {
    this.httpClient.get('http://127.0.0.1:5002/servidor/TamanhoLista/'+ '0').subscribe(data => {
      this.countUser = data as JSON;
      console.log(this.countUser);
      this.eventSource = new EventSource("http://127.0.0.1:5002/stream?channel=" + String(this.countUser) + '0')
      this.eventSource.addEventListener('publish',  (motoristaInfo:any)=>{
          console.log(motoristaInfo)
          data = String(data).replace("/", "" )
          this.motoristaInfo = String(motoristaInfo.data).replace("/", "" )
          this.openSnackBar("Encontramos uma viagem compátivel com a sua, para ver, clique na notificação", "Ok")
      },  true)
    })
    
   }
   mostrarViagemCompativel(){
     
    if(this.page == 4){
      this.page = 2;
     }else{
      this.page = 4;
     }
     var nome = this.motoristaInfo.substring(this.motoristaInfo.indexOf('\"'), this.motoristaInfo.indexOf('\",'))
     var contato = this.motoristaInfo.substring(this.motoristaInfo.indexOf('\",'), this.motoristaInfo.indexOf('\"]'))
     nome = String(nome).replace('\"', "" )
     contato = String(contato).replace('\"', "" )
     this.motoristaInfo = [nome, contato]
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
  MinhasViagens() {
    this.httpClient.get('http://127.0.0.1:5002/servidor/consultaViagensDoUsuario/' + this.IdUser  + '/0').subscribe(data => {
      this.viagensDoUsuario = data as JSON;
      console.log(this.viagensDoUsuario);
      
    })
  }
  ConsultaViagens(origem:any, destino:any, data:any) {
    data = String(data).replace("/", "" )
    data = String(data).replace("/", "" )
    this.httpClient.get('http://127.0.0.1:5002/servidor/consulta/' + origem + '/'+ destino + '/'+ data + '/0').subscribe(data => {
      this.listadeViagens = data as JSON;
      console.log(this.listadeViagens);
    })
  }

  InteresseEmCarona(origem:any, destino:any, data:any, qtdePassageiros:any) {
    data = String(data).replace("/", "" )
    data = String(data).replace("/", "" )
    if(this.IdUser){
      this.httpClient.post('http://127.0.0.1:5002/servidor/interesseEmCarona/' + this.IdUser + '/' + origem + '/'+ destino + '/'+ data + '/'+ qtdePassageiros, "").subscribe(response => {
        this.idCorrida = response  as JSON;
        console.log(this.idCorrida);
        this.MinhasViagens()
        // this.NotificaMotorista(origem, destino, data)
      })
    }else{
      console.log("SEM USUARIO")
    }
  }

  removeInteresseEmCarona(idCorrida:any) {
    this.httpClient.delete('http://127.0.0.1:5002/servidor/removeInteresseEmCarona/' + idCorrida).subscribe(data => {
      this.listadeViagens = data as JSON;
      console.log(this.listadeViagens)
    })
  }
}
