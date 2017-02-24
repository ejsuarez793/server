# from django.contrib.auth.models import User
from app.models import (Trabajador, Presupuesto, Movimiento, Proyecto,Proyecto_tecnico,
 Etapa_tecnico_movimiento, Cliente, Proveedor, Solicitud, Material, Servicio ,Material_proveedor,
 Material_movimiento, Material_presupuesto, Reporte_servicio, Servicio_presupuesto, Factura)
# from app.serializers.serializersAll import UserSerializer, TrabajadorSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
# from django.db import transaction


def viewsAdministrador(arg):
    pass


class GestionUsuario(APIView):
    permissions_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, ci, format=None):
        try:
            trabajador = Trabajador.objects.get(ci=ci)
            flag = False
            if(trabajador.cargo=="a"):
                print("almacenista")
                movimientos = Movimiento.objects.filter(ci_almace=ci)
                if not movimientos:
                    flag = True
            elif(trabajador.cargo=="c"):
                proyectos = Proyecto.objects.filter(ci_coord=ci)
                if not proyectos:
                    flag = True
                print("coordinador")
            elif(trabajador.cargo=="v"):
                presupuestos = Presupuesto.objects.filter(ci_vendedor=ci)
                if not presupuestos:
                    flag = True
                print("vendedor")
            elif(trabajador.cargo=="t"):
                print("tecnico")
                pt = Proyecto_tecnico.objects.filter(ci_tecnico=ci)
                etm = Etapa_tecnico_movimiento.objects.filter(ci_tecnico=ci)
                if(not pt and not etm):
                    flag = True
            if(flag==True):
                trabajador.cargo = request.data
                trabajador.save()

                data = {}
                data['data'] = None
                data['msg'] = "Rol de usuario cambiado exitosamente."
            else:
                return Response("El rol de usuario no se puede cambiar, ya es un usuario activo.", status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status=status.HTTP_200_OK)
        except Trabajador.DoesNotExist:
            return Response("No hay un usuario registrado con esa cedula.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ClaveUsuario(APIView):
    permissions_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, ci, format=None):
        try:
            trabajador = Trabajador.objects.get(ci=ci)
            trabajador.usuario.set_password(request.data['password1'])
            trabajador.usuario.save()
            data = {}
            data['data'] = None
            data['msg'] = "Clave de usuario cambiado exitosamente."
            return Response(data, status=status.HTTP_200_OK)
        except Trabajador.DoesNotExist:
            return Response("No hay un usuario registrado con esa cedula.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class BorrarElemento(APIView):
    permissions_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, tipo, codigo, format=None):
        with transaction.atomic():
            try: 
                error = False
                msg = ""
                lista = []
                cont =  0
                nro_elementos = 10

                if (tipo == "Cliente"):
                    print("Cliente")
                    cliente = Cliente.objects.get(rif=codigo)

                    solicitudes = Solicitud.objects.filter(rif_c = cliente.rif)
                    if not solicitudes:
                        print("no tiene solicitudes")
                    else:
                        msg = "El cliente tiene " + str(len(solicitudes)) + " solicitudes, no se puede borrar."
                        cont = 0
                        for solicitud in solicitudes:
                            if (cont > nro_elementos):
                                break
                            lista.append("Solicitud Codigo " + str(solicitud.codigo))
                        error = True





                elif (tipo == "Proveedor"):
                    print("Proveedor")
                    proveedor = Proveedor.objects.get(rif=codigo)

                    materiales_proveedor = Material_proveedor.objects.filter(codigo_prove=proveedor.rif)
                    if not materiales_proveedor:
                        print("no tiene materiales el proveedor")
                    else:
                        msg = "El proveedor tiene " + str(len(materiales_proveedor)) + " materiales asociados, no se puede borrar."
                        cont = 0
                        for material in materiales_proveedor:
                            if (cont > nro_elementos):
                                break
                            lista.append("Material Codigo " + str(material.codigo_mat.codigo))
                        error = True




                elif (tipo == "Solicitud"):
                    solicitud = Solicitud.objects.get(codigo=codigo)
                    proyecto = Proyecto.objects.get(codigo_s=solicitud.codigo)
                    msg = "La solicitud fue atendida, y se encuentra asociada al proyecto " + str(proyecto.codigo)
                    lista.append("Proyecto Codigo " + str(proyecto.codigo))
                    error = True
                    print("Solicitud")






                elif (tipo == "Material"):
                    material = Material.objects.get(codigo=codigo)

                    material_movimiento = Material_movimiento.objects.filter(codigo_mat=material.codigo)
                    if not material_movimiento:
                        print("no tiene movimmientos el material")
                    else:
                        msg = "El material tiene " + str(len(material_movimiento)) + " movimientos asociados, no se puede borrar."
                        cont = 0
                        for mm in material_movimiento:
                            if (cont > nro_elementos):
                                break
                            lista.append("Movimiento Codigo " + str(mm.codigo_mov.codigo))
                        error = True

                    material_presupuesto = Material_presupuesto.objects.filter(codigo_mat=material.codigo)
                    if not material_presupuesto:
                        print("no existen un presupuesto que tenga el material asociado")
                    else:
                        msg = "El material se encuentra en" + str(len(material_presupuesto)) + " presupuesto(s), no se puede borrar."
                        cont = 0
                        for mp in material_presupuesto:
                            if (cont > nro_elementos):
                                break
                            lista.append("Presupuesto Codigo " + str(mp.codigo_pre.codigo))
                        error = True

                    if (error is False):
                        print("no  hay problema el material se puede borrar")
                    print("Material")





                elif (tipo == "Servicio"):
                    servicio = Servicio.objects.get(codigo=codigo)

                    servicio_reporte = Reporte_servicio.objects.filter(codigo_ser=servicio.codigo)
                    if not servicio_reporte:
                        print("no tiene reportes el servicio")
                    else:
                        msg = "El servicio se encuentra " + str(len(servicio_reporte)) + " reportes asociados, no se puede borrar."
                        cont = 0
                        for sp in servicio_reporte:
                            if (cont > nro_elementos):
                                break
                            lista.append("Movimiento Codigo " + str(sp.codigo_rep.codigo))
                        error = True

                    servicio_presupuesto = Servicio_presupuesto.objects.filter(codigo_ser=servicio.codigo)
                    if not servicio_presupuesto:
                        print("no existen un presupuesto que tenga el servicio asociado")
                    else:
                        msg = "El servicio se encuentra en" + str(len(servicio_presupuesto)) + " presupuesto(s), no se puede borrar."
                        cont = 0
                        for sp in servicio_presupuesto:
                            if (cont > nro_elementos):
                                break
                            lista.append("Presupuesto Codigo " + str(sp.codigo_pre.codigo))
                        error = True

                    if (error is False):
                        print("no  hay problema el servicio se puede borrar")
                    print("Servicio")










                elif (tipo == "Proyecto"):
                    proyecto = Proyecto.objects.get(codigo=codigo)

                    presupuestos = Presupuesto.objects.filter(codigo_pro=proyecto.codigo)
                    if not presupuestos:
                        print("no tiene presupuestos el proyecto")
                    else:
                        msg = "El proyecto posee " + str(len(presupuestos)) + " presupuesto(s) asociado(s), no se puede borrar."
                        cont = 0
                        for presupuesto in presupuestos:
                            if (cont > nro_elementos):
                                break
                            lista.append("Presupuesto Codigo " + str(presupuesto.codigo))
                        error = True
                    print("Proyecto")










                elif (tipo == "Presupuesto"):
                    presupuesto = Presupuesto.objects.get(codigo=codigo)
                    if (presupuesto.estatus != "Preventa"):
                        error = True
                        msg = "El presupuesto no se encuentra en preventa, no se puede borrar."

                    facturas = Factura.objects.filter(codigo_pre=presupuesto.codigo)
                    if not facturas:
                        print("no tiene facturas el presupuesto")
                    else:
                        msg = "El presupuesto posee " + str(len(facturas)) + " factura(s) asociada(s), no se puede borrar."
                        cont = 0
                        for factura in facturas:
                            if (cont > nro_elementos):
                                break
                            lista.append("Factura Nro " + str(factura.nro_factura))
                        error = True


                    presupuesto_materiales = Material_presupuesto.objects.filter(codigo_pre=presupuesto.codigo)
                    if not presupuesto_materiales:
                        print("no tiene materiales el presupuesto")
                    else:
                        msg = "El presupuesto posee " + str(len(presupuesto_materiales)) + " materiales(s) asociads(s), no se puede borrar."
                        cont = 0
                        for presupuesto_material in presupuesto_materiales:
                            if (cont > nro_elementos):
                                break
                            lista.append("Material Codigo " + str(presupuesto_material.codigo_mat.codigo))
                        error = True


                    presupuesto_servicios = Servicio_presupuesto.objects.filter(codigo_pre=presupuesto.codigo)
                    if not presupuesto_servicios:
                        print("no tiene servicios el presupuesto")
                    else:
                        msg = "El presupuesto posee " + str(len(presupuesto_servicios)) + " servicio(s) asociads(s), no se puede borrar."
                        cont = 0
                        for presupuesto_servicio in presupuesto_servicios:
                            if (cont > nro_elementos):
                                break
                            lista.append("Servicio Codigo " + str(presupuesto_servicio.codigo_ser.codigo))
                        error = True


                    print("Presupuesto")


                print(lista)
                data = {}
                data['data'] = None
                data['msg'] = "Elemento borrado exitosamente."
                return Response(data, status=status.HTTP_200_OK)

            except (Cliente.DoesNotExist, Proveedor.DoesNotExist, Solicitud.DoesNotExist, Material.DoesNotExist, 
                    Servicio.DoesNotExist, Presupuesto.DoesNotExist):
                return Response("No existe un "+ tipo +" con codigo: " + codigo,status=status.HTTP_400_BAD_REQUEST)
            except Proyecto.DoesNotExist:
                if (tipo == "Solicitud"):
                    print ("solicitud no asociada a ningun proyecto")
                    data = {}
                    data['data'] = None
                    data['msg'] = "Elemento borrado exitosamente."
                    return Response(data, status=status.HTTP_200_OK)
                elif(tipo == "Proyecto"):
                    return Response("No existe un "+ tipo +" con codigo: " + codigo,status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)