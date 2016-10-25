package com.example.zhanghanke.together;

import android.bluetooth.BluetoothA2dp;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

import java.io.IOException;
import java.io.PrintStream;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Iterator;
import java.util.Set;
import java.util.UUID;


public class MainActivity extends ActionBarActivity {

    private Button connectButton;
    private Button beginButton;
//    private Button bluetoothButton;
    private TextView showText_x;
    private TextView showText_y;
    private TextView showText_z;

    private float mGX = 0;
    private float mGY = 0;
    private float mGZ = 0;

    private String message = "";
    private Socket socket;
    private PrintStream output;
    private String server_ip = "118.202.10.48";
    private int server_port = 9999;

//    private BluetoothAdapter adapter;
//    private BluetoothSocket bluetoothSocket;
//    private BluetoothDevice mdevice;
//    private BroadcastReceiver mReceiver;
//    private BluetoothDevice device1;

    private SensorManager mSensorMgr = null;
    Sensor mSensor = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        showText_x = (TextView) findViewById(R.id.text_show_x);
        showText_y = (TextView) findViewById(R.id.text_show_y);
        showText_z = (TextView) findViewById(R.id.text_show_z);

        connectButton = (Button) findViewById(R.id.button_connect);
        beginButton = (Button) findViewById(R.id.button_begin);
//        bluetoothButton = (Button) findViewById(R.id.button_bluetooth);

//        连接按钮操作
        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    socket = new Socket(server_ip, server_port);
                    output = new PrintStream(socket.getOutputStream(), true, "utf-8");
                    connectButton.setEnabled(false);
                } catch (UnknownHostException e) {
                    handleException(e, "Unknown host exception:" + e.toString());
                } catch (IOException e) {
                    handleException(e, "IO exception:" + e.toString());
                }
            }
        });

////        蓝牙按钮操作
//        bluetoothButton.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                adapter = BluetoothAdapter.getDefaultAdapter();
//                //打开蓝牙
//                if (adapter != null) {
//                    Log.d("a", "本机拥有蓝牙");
//                    if (!adapter.isEnabled()) {
//                        Intent intent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
//                        startActivity(intent);
//                    }
//                    //打印已匹配的蓝牙列表
//                    Set<BluetoothDevice> devices = adapter.getBondedDevices();
//                    if (devices.size() > 0) {
//                        for (Iterator iterator = devices.iterator(); iterator.hasNext(); ) {
//                            BluetoothDevice device = (BluetoothDevice) iterator.next();
//                            Log.d("mytag", device.getAddress());
//                        }
//                    }
//                } else {
//                    Log.d("b", "本机没有蓝牙");
//                }
//                mReceiver = new BroadcastReceiver() {
//                    @Override
//                    public void onReceive(Context context, Intent intent) {
//                        String action = intent.getAction();
//                        if (BluetoothDevice.ACTION_FOUND.equals(action)){
//                            device1 = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
//                            //少一句
//                        }
//                    }
//                };
//                IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
//                registerReceiver(mReceiver, filter);
//
//                mdevice = device1;
//                try{
//                    bluetoothSocket = device1.createRfcommSocketToServiceRecord(UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee"));
//                } catch (IOException e) {
//                    e.printStackTrace();
//                }
//
//                adapter.cancelDiscovery();
//                try {
//                    bluetoothSocket.connect();
//                } catch (IOException e) {
//                    try {
//                        bluetoothSocket.close();
//                    } catch (IOException e1) {
//                        e1.printStackTrace();
//                    }
//                }
//                Log.d("yes","connect success");
//            }
//
//
//        });

//        开始按钮操作
        beginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mSensorMgr = (SensorManager) getSystemService(SENSOR_SERVICE);
                mSensor = mSensorMgr.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
                SensorEventListener lsn = new SensorEventListener() {
                    @Override
                    public void onSensorChanged(SensorEvent event) {
                        float x = event.values[SensorManager.DATA_X];
                        float y = event.values[SensorManager.DATA_Y];
                        float z = event.values[SensorManager.DATA_Z];
                        mGX = x;
                        mGY = y;
                        mGZ = z;
                        if (mGX >= 10.0) {
                            mGX = (float) 9.99999;
                        } else if (mGX <= -10.0) {
                            mGX = (float) -9.99999;
                        }
                        if (mGY >= 10.0) {
                            mGY = (float) 9.99999;
                        } else if (mGX <= -10.0) {
                            mGY = (float) -9.99999;
                        }
                        if (mGZ >= 10.0) {
                            mGZ = (float) 9.99999;
                        } else if (mGX <= -10.0) {
                            mGY = (float) -9.99999;
                        }
                        message = "x=" + mGX + ";" + "y=" + mGY + ";" + "z=" + mGZ + ";";
                        showText_x.setText("x=" + mGX);
                        showText_y.setText("y=" + mGY);
                        showText_z.setText("z=" + mGZ);
                        output.print(message);

                    }

                    @Override
                    public void onAccuracyChanged(Sensor sensor, int accuracy) {
                    }
                };
                mSensorMgr.registerListener(lsn, mSensor, SensorManager.SENSOR_DELAY_GAME);
            }
        });

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void toastText(String message) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }


    public void handleException(Exception e, String prefix) {
        e.printStackTrace();
        toastText(prefix + e.toString());
    }


}
