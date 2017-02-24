# from django.contrib.auth.models import User
from app.models import (Trabajador, Presupuesto, Movimiento, Proyecto,Proyecto_tecnico,
 Etapa_tecnico_movimiento, Cliente, Proveedor, Solicitud, Material, Servicio ,Material_proveedor,
 Material_movimiento, Material_presupuesto, Reporte_servicio, Servicio_presupuesto, Factura, Proyecto_tecnico)
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
                # print("almacenista")
                movimientos = Movimiento.objects.filter(ci_almace=ci)
                if not movimientos:
                    flag = True
            elif(trabajador.cargo=="c"):
                proyectos = Proyecto.objects.filter(ci_coord=ci)
                if not proyectos:
                    flag = True
                # print("coordinador")
            elif(trabajador.cargo=="v"):
                presupuestos = Presupuesto.objects.filter(ci_vendedor=ci)
                if not presupuestos:
                    flag = True
                # print("vendedor")
            elif(trabajador.cargo=="t"):
                # print("tecnico")
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
                msg2 = ""
                msg3 = ""
                lista = []
                lista2 = []
                lista3 = []
                cont =  0
                nro_elementos = 10

                if (tipo == "Cliente"):
                    cliente = Cliente.objects.get(rif=codigo)

                    solicitudes = Solicitud.objects.filter(rif_c = cliente.rif)
                    if not solicitudes:
                        cliente.delete()
                    else:
                        msg = "El cliente tiene " + str(len(solicitudes)) + " solicitud(es), no se puede borrar."
                        cont = 0
                        for solicitud in solicitudes:
                            if (cont > nro_elementos):
                                break
                            lista.append("Solicitud Codigo " + str(solicitud.codigo))
                        error = True





                elif (tipo == "Proveedor"):
                    proveedor = Proveedor.objects.get(rif=codigo)

                    materiales_proveedor = Material_proveedor.objects.filter(codigo_prove=proveedor.rif)
                    if not materiales_proveedor:
                        proveedor.delete()
                    else:
                        msg = "El proveedor tiene " + str(len(materiales_proveedor)) + " material(es) asociado(s), no se puede borrar."
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





                elif (tipo == "Material"):
                    material = Material.objects.get(codigo=codigo)

                    material_movimiento = Material_movimiento.objects.filter(codigo_mat=material.codigo)
                    if material_movimiento:
                        msg = "El material tiene " + str(len(material_movimiento)) + " movimiento(s) asociado(s), no se puede borrar."
                        cont = 0
                        for mm in material_movimiento:
                            if (cont > nro_elementos):
                                break
                            lista.append("Movimiento Codigo " + str(mm.codigo_mov.codigo))
                        error = True

                    material_presupuesto = Material_presupuesto.objects.filter(codigo_mat=material.codigo)
                    if material_presupuesto:
                        msg2 = "El material se encuentra en " + str(len(material_presupuesto)) + " presupuesto(s), no se puede borrar."
                        cont = 0
                        for mp in material_presupuesto:
                            if (cont > nro_elementos):
                                break
                            lista2.append("Presupuesto Codigo " + str(mp.codigo_pre.codigo))
                        error = True

                    if (error is False):
                        Material_proveedor.objects.filter(codigo_mat=material.codigo).delete()
                        material.delete()






                elif (tipo == "Servicio"):
                    servicio = Servicio.objects.get(codigo=codigo)

                    servicio_reporte = Reporte_servicio.objects.filter(codigo_ser=servicio.codigo)
                    if servicio_reporte:
                        msg = "El servicio se encuentra " + str(len(servicio_reporte)) + " reporte(s), no se puede borrar."
                        cont = 0
                        for sp in servicio_reporte:
                            if (cont > nro_elementos):
                                break
                            lista.append("Movimiento Codigo " + str(sp.codigo_rep.codigo))
                        error = True

                    servicio_presupuesto = Servicio_presupuesto.objects.filter(codigo_ser=servicio.codigo)
                    if servicio_presupuesto:
                        msg2 = "El servicio se encuentra en " + str(len(servicio_presupuesto)) + " presupuesto(s), no se puede borrar."
                        cont = 0
                        for sp in servicio_presupuesto:
                            if (cont > nro_elementos):
                                break
                            lista2.append("Presupuesto Codigo " + str(sp.codigo_pre.codigo))
                        error = True

                    if (error is False):
                        servicio.delete()











                elif (tipo == "Proyecto"):
                    proyecto = Proyecto.objects.get(codigo=codigo)
                    if (proyecto.estatus != "Preventa" ):
                        error = True
                        msg = "El estado del proyecto '" + proyecto.estatus + "' no permite borrarlo."
                    else:
                        presupuestos = Presupuesto.objects.filter(codigo_pro=proyecto.codigo)
                        if presupuestos:
                            msg = "El proyecto posee " + str(len(presupuestos)) + " presupuesto(s) asociado(s), no se puede borrar."
                            cont = 0
                            for presupuesto in presupuestos:
                                if (cont > nro_elementos):
                                    break
                                lista.append("Presupuesto Codigo " + str(presupuesto.codigo))
                            error = True

                    if (error is False):
                        Proyecto_tecnico.objects.filter(codigo_pro=proyecto.codigo).delete()
                        proyecto.delete()









                elif (tipo == "Presupuesto"):
                    presupuesto = Presupuesto.objects.get(codigo=codigo)
                    if (presupuesto.estatus != "Preventa"):
                        error = True
                        msg = "El presupuesto no se encuentra en preventa, no se puede borrar."
                    else:
                        facturas = Factura.objects.filter(codigo_pre=presupuesto.codigo)
                        if facturas:
                            msg = "El presupuesto posee " + str(len(facturas)) + " factura(s) asociada(s), no se puede borrar."
                            cont = 0
                            for factura in facturas:
                                if (cont > nro_elementos):
                                    break
                                lista.append("Factura Nro " + str(factura.nro_factura))
                            error = True


                        presupuesto_materiales = Material_presupuesto.objects.filter(codigo_pre=presupuesto.codigo)
                        if presupuesto_materiales:
                            msg2 = "El presupuesto posee " + str(len(presupuesto_materiales)) + " materiales(s) asociads(s), no se puede borrar."
                            cont = 0
                            for presupuesto_material in presupuesto_materiales:
                                if (cont > nro_elementos):
                                    break
                                lista2.append("Material Codigo " + str(presupuesto_material.codigo_mat.codigo))
                            error = True


                        presupuesto_servicios = Servicio_presupuesto.objects.filter(codigo_pre=presupuesto.codigo)
                        if presupuesto_servicios:
                            msg3 = "El presupuesto posee " + str(len(presupuesto_servicios)) + " servicio(s) asociads(s), no se puede borrar."
                            cont = 0
                            for presupuesto_servicio in presupuesto_servicios:
                                if (cont > nro_elementos):
                                    break
                                lista3.append("Servicio Codigo " + str(presupuesto_servicio.codigo_ser.codigo))
                            error = True


                    if (error is False):
                        presupuesto.delete()


                print(lista)
                data = {}
                data['error'] = error
                data['msg'] = []
                data['listas'] = []
                aux={}
                aux2={}
                aux3={}
                if (error is False):
                    data['msg'] = "Elemento borrado exitosamente."
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    if lista and msg != "":
                        aux['msg'] = msg
                        aux['lista'] = lista
                        data['listas'].append(aux)
                    if lista2 and msg2 != "":
                        aux2['msg'] = msg2
                        aux2['lista'] = lista2
                        data['listas'].append(aux2)
                    if lista3 and msg3 != "":
                        aux3['msg'] = msg3
                        aux3['lista'] = lista3
                        data['listas'].append(aux3)

                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

            except (Cliente.DoesNotExist, Proveedor.DoesNotExist, Solicitud.DoesNotExist, Material.DoesNotExist, 
                    Servicio.DoesNotExist, Presupuesto.DoesNotExist):
                data = {}
                data['data'] = None
                data['error'] = True
                data['msg'] = "No existe un "+ tipo +" con codigo: " + codigo
                return Response(data,status=status.HTTP_404_NOT_FOUND)
            except Proyecto.DoesNotExist:
                if (tipo == "Solicitud"):
                    solicitud = Solicitud.objects.get(codigo=codigo).delete()
                    data = {}
                    data['data'] = None
                    data['msg'] = "Elemento borrado exitosamente."
                    return Response(data, status=status.HTTP_200_OK)
                elif(tipo == "Proyecto"):
                    data = {}
                    data['data'] = None
                    data['error'] = True
                    data['msg'] = "No existe un "+ tipo +" con codigo: " + codigo
                    return Response(data,status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)