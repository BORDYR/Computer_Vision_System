using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading;
using System.IO.Ports;

namespace SendMes
{
    class MainClass
    {
        
            public static void Main(string[] args)
        {
            Char End = (char)13;
            SerialPort serialPort1 = new SerialPort();
            serialPort1.PortName = "COM3";
            String testStr = "RS\nMO 105";

            serialPort1.Handshake = System.IO.Ports.Handshake.RequestToSend;
            serialPort1.Parity = System.IO.Ports.Parity.Even;
            serialPort1.PortName = "COM3";
            serialPort1.WriteTimeout = 100;
            Console.WriteLine("11");
            if (!serialPort1.IsOpen)
            {
                serialPort1.Open();
            }
            Console.WriteLine(serialPort1.IsOpen);

            

            string[] Lines = testStr.Split('\n');
            Console.WriteLine(testStr);

            
                for (int i = 0; i < Lines.Count(); i++)
                {
                    if (!serialPort1.IsOpen) Console.WriteLine('1');
                    if (serialPort1.IsOpen) serialPort1.Write(Lines[i].Trim() + End);
                }
            
            
        }
    }
}