/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     13/03/2025 18:23:45                          */
/*==============================================================*/


alter table Client 
   drop foreign key FK_CLIENT_ASSOCIATI_COLLABOR;

alter table Collaborator 
   drop foreign key FK_COLLABOR_ASSOCIATI_ROLE;

alter table Contract 
   drop foreign key FK_CONTRACT_ASSOCIATI_COLLABOR;

alter table Contract 
   drop foreign key FK_CONTRACT_ASSOCIATI_CLIENT;

alter table Event 
   drop foreign key FK_EVENT_ASSOCIATI_COLLABOR;

alter table Event 
   drop foreign key FK_EVENT_ASSOCIATI_CONTRACT;


alter table Client 
   drop foreign key FK_CLIENT_ASSOCIATI_COLLABOR;

drop table if exists Client;


alter table Collaborator 
   drop foreign key FK_COLLABOR_ASSOCIATI_ROLE;

drop table if exists Collaborator;


alter table Contract 
   drop foreign key FK_CONTRACT_ASSOCIATI_COLLABOR;

alter table Contract 
   drop foreign key FK_CONTRACT_ASSOCIATI_CLIENT;

drop table if exists Contract;


alter table Event 
   drop foreign key FK_EVENT_ASSOCIATI_COLLABOR;

alter table Event 
   drop foreign key FK_EVENT_ASSOCIATI_CONTRACT;

drop table if exists Event;

drop table if exists Role;

/*==============================================================*/
/* Table: Client                                                */
/*==============================================================*/
create table Client
(
   id                   int not null  comment '',
   Col_id               int not null  comment '',
   first_name           varchar(50)  comment '',
   last_name            varchar(50)  comment '',
   email                varchar(120)  comment '',
   phone                varchar(20)  comment '',
   company_name         varchar(100)  comment '',
   first_contact_date   datetime  comment '',
   last_contact_date    datetime  comment '',
   primary key (id)
);

/*==============================================================*/
/* Table: Collaborator                                          */
/*==============================================================*/
create table Collaborator
(
   id                   int not null  comment '',
   Rol_id               int not null  comment '',
   first_name           varchar(50)  comment '',
   last_name            varchar(50)  comment '',
   email                varchar(120)  comment '',
   password_hash        varchar(128)  comment '',
   primary key (id)
);

/*==============================================================*/
/* Table: Contract                                              */
/*==============================================================*/
create table Contract
(
   id                   int not null  comment '',
   Cli_id               int not null  comment '',
   Col_id               int not null  comment '',
   costing              float  comment '',
   remaining_due_payment float  comment '',
   creation_date        datetime  comment '',
   is_signed            bool  comment '',
   primary key (id),
   key AK_Identifier_1 (id)
);

/*==============================================================*/
/* Table: Event                                                 */
/*==============================================================*/
create table Event
(
   id                   int not null  comment '',
   Con_id               int not null  comment '',
   Col_id               int  comment '',
   name                 varchar(100)  comment '',
   start_date           datetime  comment '',
   end_date             datetime  comment '',
   location             varchar(255)  comment '',
   attendees            int  comment '',
   notes                text  comment '',
   primary key (id)
);

/*==============================================================*/
/* Table: Role                                                  */
/*==============================================================*/
create table Role
(
   id                   int not null  comment '',
   name                 varchar(50)  comment '',
   primary key (id)
);

alter table Client add constraint FK_CLIENT_ASSOCIATI_COLLABOR foreign key (Col_id)
      references Collaborator (id) on delete restrict on update restrict;

alter table Collaborator add constraint FK_COLLABOR_ASSOCIATI_ROLE foreign key (Rol_id)
      references Role (id) on delete restrict on update restrict;

alter table Contract add constraint FK_CONTRACT_ASSOCIATI_COLLABOR foreign key (Col_id)
      references Collaborator (id) on delete restrict on update restrict;

alter table Contract add constraint FK_CONTRACT_ASSOCIATI_CLIENT foreign key (Cli_id)
      references Client (id) on delete restrict on update restrict;

alter table Event add constraint FK_EVENT_ASSOCIATI_COLLABOR foreign key (Col_id)
      references Collaborator (id) on delete restrict on update restrict;

alter table Event add constraint FK_EVENT_ASSOCIATI_CONTRACT foreign key (Con_id)
      references Contract (id) on delete restrict on update restrict;

