using UnityEngine;
using System.IO;
using System.Collections.Generic;
using System;

namespace Sky
{
    public class StarDataLoader
    {

        public List<Star> LoadData(string filename = "BSC5")
        {
            List<Star> stars = new();
            TextAsset textAsset = Resources.Load(filename) as TextAsset;
            MemoryStream stream = new(textAsset.bytes);
            BinaryReader br = new(stream);
            // Subtract from star number to get sequence number
            int sequence_offset = br.ReadInt32();
            // First star number in file
            int star_index = br.ReadInt32();
            // Number of stars in file
            int num_stars = br.ReadInt32();
            // 0 if no star i.d. numbers are present
			// 1 if star i.d. numbers are in catalog file
			// 2 if star i.d. numbers are  in file
            int star_number_settings = br.ReadInt32();
            // 1 if proper motion is included
			// 0 if no proper motion is included
            int proper_motion_included = br.ReadInt32();
            // Number of magnitudes present (-1=J2000 instead of B1950)
            int num_magnitudes = br.ReadInt32();
            // Number of bytes per star entry
            int star_data_size = br.ReadInt32();    

            int year; 
            // number of star is negative if the coordinates are j2000 (from 2000) rather than b1950(from 1950)
            if (num_stars < 0 || num_magnitudes == -1)
            {
                year = 2000;
                num_stars = Math.Abs(num_stars); 
            }            
            else
            {
                year = 1950; 
            }

            for (int i = 0; i < num_stars; i++)
            {
                float catalog_number = br.ReadSingle();
                double right_ascension = br.ReadDouble();
                // Angular distance from celestial equator.
                // B1950 Declination (radians)
                double declination = br.ReadDouble();
                // Spectral type (2 characters)
                byte spectral_type = br.ReadByte();
                byte spectral_index = br.ReadByte();
                // V Magnitude * 100
                short magnitude = br.ReadInt16();
                // R.A. proper motion (radians per year) [optional]
                float ra_proper_motion = br.ReadSingle();
                // Dec. proper motion (radians per year) [optional]
                float dec_proper_motion = br.ReadSingle();
                Star star = new(catalog_number, right_ascension, declination, spectral_type, spectral_index, magnitude, ra_proper_motion, dec_proper_motion, year);
                stars.Add(star);
            }

            return stars;
        }

    }
}

