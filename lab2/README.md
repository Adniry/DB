#  КВ-82 Гольовський Андрій
##  Лабораторна робота №2
### Ознайомлення з базовими операціями СУБД PostgreSQL

**[Посилання](https://drive.google.com/file/d/12oANW7DdS6wAUis_FbgTPr1gGFRKAYSp/view?usp=sharing) на документ з описом структури БД**  
   
   **Сутності**
1) **Людина:**
  - pid;
  - Ім'я;
  - Прізвище.
  ```
CREATE TABLE public.person
(
    pid integer NOT NULL,
    name character(30) COLLATE pg_catalog."default" NOT NULL,
    surname character(30) COLLATE pg_catalog."default" NOT NULL,
    exemption character(30) COLLATE pg_catalog."default",
    CONSTRAINT "PID" PRIMARY KEY (pid)
)

    
 ```

2) **Транспорт:**
  - номер авто;
  - номер маршруту.
  ```
CREATE TABLE public.transport
(
    car_number integer NOT NULL,
    route_number integer NOT NULL,
    CONSTRAINT "Transport_pkey" PRIMARY KEY (car_number)
)
  ```
3) **Зупинка:**
  - sid;
  - адреса.
  ``` 
CREATE TABLE public.stop
(
    sid integer NOT NULL,
    address character(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Stop_pkey" PRIMARY KEY (sid)
)
 ```
4) **Квиток:**
  - tid;
  - ціна;
  - дійсний до.
  ```
CREATE TABLE public.ticket
(
    tid integer NOT NULL,
    price numeric NOT NULL,
    operation_time timestamp without time zone NOT NULL,
    CONSTRAINT "TID" PRIMARY KEY (tid)
)
  ```
  
5) **ownership:**
  - pid;
  - tid.
  ```
 CREATE TABLE public.ownership
(
    tid integer NOT NULL,
    pid integer,
    CONSTRAINT "Ownership_pkey" PRIMARY KEY (tid),
    CONSTRAINT "PID" FOREIGN KEY (pid)
        REFERENCES public.person (pid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "TID" FOREIGN KEY (tid)
        REFERENCES public.ticket (tid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
  ```
6) **розклад:**
  - scheduleid;
  - номер авто;
  - sid;
  - час прибуття.

  ```
CREATE TABLE public.schedule
(
    scheduleid integer NOT NULL,
    car_number integer NOT NULL,
    sid integer NOT NULL,
    "time" time without time zone NOT NULL,
    CONSTRAINT "ScheduleID" PRIMARY KEY (scheduleid),
    CONSTRAINT "Car_number" FOREIGN KEY (car_number)
        REFERENCES public.transport (car_number) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "SID" FOREIGN KEY (sid)
        REFERENCES public.stop (sid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
  ```
7) **поїздка:**
  - tripid;
  - car_number;
  - tid;
  - чвс початку;
  - час кінця.

 ``` 
CREATE TABLE public.trip
(
    tripid integer NOT NULL,
    car_number integer NOT NULL,
    tid integer NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    CONSTRAINT tripid PRIMARY KEY (tripid),
    CONSTRAINT car_number FOREIGN KEY (car_number)
        REFERENCES public.transport (car_number) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT tid FOREIGN KEY (tid)
        REFERENCES public.ticket (tid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
 ```

