class Empleado:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.odata_etag = kwargs.get('@odata.etag')
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
        """

        
    def __init__(self):
        self.SiglaNacion = None
        self.Dni = None
        self.CodigoEmpleado = None
        self.NombreEmpleado = None
        self.ProvNumSoe = None
        self.PrimerApellidoEmpleado = None
        self.SegundoApellidoEmpleado = None
        self.CodigoPostal = None
        self.DireccionCompleta = None
        self.Telefono = None
        self.TelefonoMovil = None
        self.Municipio = None
        self.Provincia = None
        self.Sexo = None
        self.FechaNacimiento = None
        self.EMail1 = None
        self.FechaInicioContrato = None
        self.FechaFinalContrato = None
        self.IBANReceptor = None
        self.odata_etag = None



