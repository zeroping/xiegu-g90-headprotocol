from construct import *
from construct.lib import *

#this was orignally generated from Kaitai, but didn't totally work, so it's been manually patched up, and the added to.

def xiegug90head__att_modes(subcon):
	return Enum(subcon,
		none=0,
		pre=1,
		att=2,
	)

def xiegug90head__modulations(subcon):
	return Enum(subcon,
		lsb=0,
		usb=1,
		cw=2,
		crr=3,
		nfm=4,
		fm=5,
	)

def xiegug90head__gain_modes(subcon):
	return Enum(subcon,
		false=0,
		slow=1,
		fast=2,
		auto=3,
	)



xiegug90head = Struct(
	'header' / Default(Array(2, Byte), [0x55, 0xaa]),
	'pad1' / Int16ub,
	'freq1' / Default(Int32ul, 28410000),
	'att_mode' / xiegug90head__att_modes(Int8ub),
	'modulation' / xiegug90head__modulations(Int8ub),
	'agc' / xiegug90head__gain_modes(Int8ub),
	'pad2' / Int8ub,
	'filter_high_raw' / Int8ub,
	'filter_low_raw' / Int8ub,
	#byte 14
	'pad3' / Array(5, Byte),
	#byte 19
	'fft_gain' / Int8ub,
	'freq2' / Int32ul,
	'pad5' / Array(12, Byte),
	'ctrl1' / BitStruct(
          'transmit' / Flag, #0x80
          'vfo_en' / Flag,
          'tuner_en' / Flag,
          'nb_en' / Flag,
          'mic_compression' / Flag,
          'output_headphones' / Flag,
          'split_en' / Flag,
          'panel_lock' / Flag,
	),
        #37
        'ctrl2' / BitStruct(
          'shutdown_req' / Flag, # not sure, just observed right before powerdown
          Padding(1),
          'tuning' / Flag, #0x20
          Padding(5),
	),
        #38
        'ctrl3' / BitStruct(
          'rclk_raw_low' / BitsInteger(3),
          'cw_disp_en' / Flag,
          'vox_en' / Flag,
          'audio_in_line_en' / Flag,
          'tx_disable' / Flag,
          'cw_qsk' / Flag,
	),
        'rclk_raw_high' / Int8ub,
        
        'ctrl4' / BitStruct(
          #40
          'vox_anti_gain_low' / BitsInteger(1),
          'vox_gain' / BitsInteger(7),
          #41
          'vox_delay_low' / BitsInteger(2),
          'vox_anti_gain_high' / BitsInteger(6),
          #42
          'gain_low' / BitsInteger(5),
          'vox_delay_high' / BitsInteger(3),
          #43
          Padding(4),
          'beep_en' / Flag,
          'band_stack_full' / Flag,
          'gain_high' / BitsInteger(2),
        ),
        #44
        'rf_power' / Int8ub,
        'sql_level' / Int8ub,
          'ctrl5' / BitStruct(
          'nb_level' / BitsInteger(4),
          'nb_width' / BitsInteger(4),          
	),
        Padding(1),
        #48
        'volume' / Int8ub, #0-28
        'mic_gain' / Int8ub, #0-20
        'unknown1' / Default(Byte, 0x50),
        'cq_qsk_time_raw' / Int8ub, #0-20
        'unknown2' / Default(Byte, 0x01),
        'mem_ch' / Int8ub, #0-20
        #54
        'ctrl6' / BitStruct(
          Padding(7),
          'vfo_b_en' / Flag,
	),
        Padding(1),
        'unknown3' / Default(Array(4, Byte), [0xff, 0xff, 0xff, 0xff]),
        #60
        'cw_wpm' / Int8ub, #5-50 wpm
        'ctrl7' / BitStruct(
          'cw_ratio_raw' / BitsInteger(4),
          Padding(1),
          'cw_mode_b' / Flag,
          'cw_mlr' / BitsInteger(2),
	),
        #Padding(20),
        'unknown4' / Default(Array(20, Byte), [0xff, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x1f, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x32]),
        #82
        'ctrl8' / BitStruct(
          Padding(4),
          'swr_threshold_raw' / BitsInteger(4),
          'aux_out_vol' / BitsInteger(4),
          'aux_in_vol' / BitsInteger(4),
        ),
        #84
        'ctrl9' / BitStruct(
          'ritval_low' / BitsInteger(8),
          Padding(6),
          'ritval_high' / BitsInteger(2),
        ),
        'unknown5' / Default(Array(6, Byte), [0xff, 0xff, 0x00, 0x00, 0x00, 0x00]),
        'checksum' / Int32ul,
        
        #computed
	'filter_low' / Computed(lambda this: (100 + (this.filter_low_raw * 25))),
	'filter_high' / Computed(lambda this: (125 + (this.filter_high_raw * 25))),
	'rclk_tune' / Computed(lambda this: ((this.rclk_raw_high << 3) + this.ctrl3.rclk_raw_low) - 1000 ),
	'vox_anti_gain'  / Computed(lambda this: ((this.ctrl4.vox_anti_gain_high << 1) + this.ctrl4.vox_anti_gain_low) ),
	'vox_delay'  / Computed(lambda this: ((this.ctrl4.vox_delay_high << 2) + this.ctrl4.vox_delay_low) /10. ),
	'gain'  / Computed(lambda this: ((this.ctrl4.gain_high << 5) + this.ctrl4.gain_low) ),
	'cw_qsk_time' / Computed(lambda this: ((this.cq_qsk_time_raw * 100))),
	'cw_ratio' / Computed(lambda this: ( 2 + (this.ctrl7.cw_ratio_raw /10.))),
	'swr_threshold' / Computed(lambda this: ( 1.8 + (this.ctrl8.swr_threshold_raw *0.2))),
	'ritval1'  / Computed(lambda this: ((((this.ctrl9.ritval_high *256) + this.ctrl9.ritval_low) +512)%1024)-512),
	
)

_schema = xiegug90head
