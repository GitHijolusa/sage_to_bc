class Empleado:
    def __init__(self):
        self.CodigoEmpleado = None
        self.NombreEmpleado = None
        self.SegundoApellidoEmpleado = None
        self.PrimerApellidoEmpleado = None
        self.DireccionCompleta = None
        self.Municipio = None
        self.CodigoPostal = None
        self.Provincia = None
        self.Telefono = None
        self.TelefonoMovil = None
        self.EMail1 = None
        self.FechaNacimiento = None
        self.ProvNumSoe = None
        self.Sexo = None
        self.SiglaNacion = None
        self.FechaInicioContrato = None
        self.FechaFinalContrato = None
        self.IBANReceptor = None
        self.Dni = None
        self.odata_etag = None
        self.estado = None
    def __str__(self):
        return f"""
        SiglaNacion: {self.SiglaNacion}
        Dni: {self.Dni}
        CodigoEmpleado: {self.CodigoEmpleado}
        NombreEmpleado: {self.NombreEmpleado}
        ProvNumSoe: {self.ProvNumSoe}
        PrimerApellidoEmpleado: {self.PrimerApellidoEmpleado}
        SegundoApellidoEmpleado: {self.SegundoApellidoEmpleado}
        CodigoPostal: {self.CodigoPostal}
        DireccionCompleta: {self.DireccionCompleta}
        Telefono: {self.Telefono}
        TelefonoMovil: {self.TelefonoMovil}
        Municipio: {self.Municipio}
        Provincia: {self.Provincia}
        Sexo: {self.Sexo}
        FechaNacimiento: {self.FechaNacimiento}
        EMail1: {self.EMail1}
        FechaInicioContrato: {self.FechaInicioContrato}
        FechaFinalContrato: {self.FechaFinalContrato}
        IBANReceptor: {self.IBANReceptor}
        Estado: {self.estado}
        """

        




